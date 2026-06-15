"""Messagerie privée support : client ↔ équipe admin (inbox partagée)."""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Conversation, DirectMessage, DirectMessageAttachment
from .notify import notify_support_message
from .typing import set_typing, typing_names
from .views import (
    ALLOWED_IMAGE_TYPES,
    FEED_LIMIT,
    MAX_IMAGES,
    MAX_IMAGE_SIZE,
    _author_label,
    parse_duration,
    validate_audio,
)

staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff)


# ── Sérialisation ───────────────────────────────────────────────────────────
def _dm_label(dm):
    if dm.is_admin:
        return "Équipe Hayiti's"
    return _author_label(dm.sender) if dm.sender else "Client"


def _excerpt(dm):
    if dm.content:
        return dm.content[:80]
    if dm.audio:
        return "🎤 note vocale"
    return "📷 image"


def serialize_dm(dm, request):
    reply = None
    if dm.reply_to_id and dm.reply_to:
        rt = dm.reply_to
        reply = {"id": rt.id, "sender": _dm_label(rt), "excerpt": _excerpt(rt)}
    # Accusé de lecture : visible UNIQUEMENT par l'admin, sur les messages de l'équipe,
    # et seulement si le client n'a pas désactivé ses accusés de lecture (confidentialité).
    viewer_staff = request.user.is_authenticated and request.user.is_staff
    client_allows = dm.conversation.client.read_receipts
    read = dm.read_by_client if (viewer_staff and dm.is_admin and client_allows) else None
    return {
        "id": dm.id,
        "is_admin": dm.is_admin,
        "sender": _dm_label(dm),
        "content": dm.content,
        "reply_to": reply,
        "attachments": [a.image.url for a in dm.attachments.all()],
        "audio": dm.audio.url if dm.audio else None,
        "audio_duration": dm.audio_duration,
        "read": read,
        "created_at": dm.created_at.isoformat(),
        "is_own": bool(request.user.is_authenticated and dm.sender_id == request.user.id),
    }


def _feed_qs(conversation):
    return (
        conversation.messages
        .select_related("sender", "reply_to", "reply_to__sender", "conversation__client")
        .prefetch_related("attachments")
    )


def _validate_images(request):
    images = request.FILES.getlist("images")[:MAX_IMAGES]
    for f in images:
        if f.size == 0:
            return None, "Image vide (0 octet)."
        if f.size > MAX_IMAGE_SIZE:
            return None, "Image trop lourde (5 Mo max)."
        if f.content_type not in ALLOWED_IMAGE_TYPES:
            return None, "Format d'image non supporté."
    return images, None


def _send_message(conversation, sender, is_admin, content, images, reply_to=None,
                  audio=None, audio_duration=0):
    dm = DirectMessage.objects.create(
        conversation=conversation, sender=sender, is_admin=is_admin, content=content,
        reply_to=reply_to, read_by_admin=is_admin, read_by_client=not is_admin,
        audio=audio, audio_duration=audio_duration if audio else 0,
    )
    for f in images:
        DirectMessageAttachment.objects.create(message=dm, image=f)
    conversation.last_message_at = dm.created_at
    conversation.save(update_fields=["last_message_at", "updated_at"])
    transaction.on_commit(lambda: notify_support_message(dm))
    return dm


def _feed_response(request, conversation):
    qs = _feed_qs(conversation)
    after = request.GET.get("after")
    before = request.GET.get("before")
    if after:
        msgs = list(qs.filter(id__gt=after).order_by("created_at")[:100])
    elif before:
        msgs = list(qs.filter(id__lt=before).order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    else:
        msgs = list(qs.order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    data = [serialize_dm(m, request) for m in msgs]
    # Pour l'admin : ids des messages de l'équipe déjà lus par le client (maj des accusés au polling)
    read_ids = []
    if request.user.is_authenticated and request.user.is_staff and conversation.client.read_receipts:
        read_ids = list(
            conversation.messages.filter(is_admin=True, read_by_client=True)
            .order_by("-id").values_list("id", flat=True)[:100]
        )
    typing = typing_names("conv", conversation.id, request.user.id)
    return JsonResponse({
        "messages": data,
        "last_id": data[-1]["id"] if data else (after or 0),
        "read_ids": read_ids,
        "typing": typing,
    })


# ── Côté CLIENT ─────────────────────────────────────────────────────────────
def support_home(request):
    if not request.user.is_authenticated:
        return render(request, "community/support_login_prompt.html")
    if request.user.is_staff:
        return redirect("community:inbox")
    conv, _ = Conversation.objects.get_or_create(client=request.user)
    # marquer comme lus les messages de l'équipe
    conv.messages.filter(is_admin=True, read_by_client=False).update(read_by_client=True)
    msgs = list(_feed_qs(conv).order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    return render(request, "community/conversation.html", {
        "is_admin_view": False,
        "conversation": conv,
        "peer_name": "Équipe Hayiti's",
        "initial_messages": [serialize_dm(m, request) for m in msgs],
        "last_id": msgs[-1].id if msgs else 0,
        "feed_url": "/community/support/feed/",
        "post_url": "/community/support/post/",
        "typing_url": "/community/support/typing/",
        "back_url": "",
        "read_receipts": request.user.read_receipts,
    })


@login_required
@require_GET
def support_feed(request):
    conv, _ = Conversation.objects.get_or_create(client=request.user)
    conv.messages.filter(is_admin=True, read_by_client=False).update(read_by_client=True)
    return _feed_response(request, conv)


@login_required
@require_POST
def support_post(request):
    if request.user.is_staff:
        return JsonResponse({"error": "Les admins répondent depuis la boîte de réception."}, status=400)
    conv, _ = Conversation.objects.get_or_create(client=request.user)
    content = (request.POST.get("content") or "").strip()
    images, err = _validate_images(request)
    if err:
        return JsonResponse({"error": err}, status=400)
    audio = request.FILES.get("audio")
    audio_duration = parse_duration(request.POST.get("audio_duration"))
    audio_err = validate_audio(audio, audio_duration)
    if audio_err:
        return JsonResponse({"error": audio_err}, status=400)
    if not content and not images and not audio:
        return JsonResponse({"error": "Message vide."}, status=400)
    reply_to = None
    rid = request.POST.get("reply_to")
    if rid:
        reply_to = DirectMessage.objects.filter(id=rid, conversation=conv).first()
    dm = _send_message(conv, request.user, is_admin=False, content=content, images=images,
                       reply_to=reply_to, audio=audio, audio_duration=audio_duration)
    return JsonResponse({"message": serialize_dm(_feed_qs(conv).get(id=dm.id), request)}, status=201)


# ── Côté ADMIN (inbox partagée) ─────────────────────────────────────────────
@staff_required
def inbox(request):
    q = (request.GET.get("q") or "").strip()
    convs = (
        Conversation.objects.select_related("client")
        .annotate(unread=Count("messages", filter=Q(messages__is_admin=False, messages__read_by_admin=False)))
        .filter(last_message_at__isnull=False)
    )
    if q:
        convs = convs.filter(Q(client__username__icontains=q) | Q(client__first_name__icontains=q) | Q(client__last_name__icontains=q))
    items = []
    for c in convs:
        last = c.messages.order_by("-created_at").first()
        items.append({
            "id": c.id,
            "client": _author_label(c.client),
            "unread": c.unread,
            "last": (last.content[:60] if last and last.content else ("📷 image" if last else "")),
            "last_at": c.last_message_at,
            "from_admin": last.is_admin if last else False,
        })
    return render(request, "community/inbox.html", {"conversations": items, "q": q})


@staff_required
def inbox_conversation(request, conv_id):
    conv = get_object_or_404(Conversation.objects.select_related("client"), id=conv_id)
    conv.messages.filter(is_admin=False, read_by_admin=False).update(read_by_admin=True)
    msgs = list(_feed_qs(conv).order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    return render(request, "community/conversation.html", {
        "is_admin_view": True,
        "conversation": conv,
        "peer_name": _author_label(conv.client),
        "initial_messages": [serialize_dm(m, request) for m in msgs],
        "last_id": msgs[-1].id if msgs else 0,
        "feed_url": f"/community/inbox/{conv.id}/feed/",
        "post_url": f"/community/inbox/{conv.id}/post/",
        "typing_url": f"/community/inbox/{conv.id}/typing/",
        "back_url": "/community/inbox/",
    })


@staff_required
@require_GET
def inbox_feed(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)
    conv.messages.filter(is_admin=False, read_by_admin=False).update(read_by_admin=True)
    return _feed_response(request, conv)


@staff_required
@require_POST
def inbox_post(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)
    content = (request.POST.get("content") or "").strip()
    images, err = _validate_images(request)
    if err:
        return JsonResponse({"error": err}, status=400)
    audio = request.FILES.get("audio")
    audio_duration = parse_duration(request.POST.get("audio_duration"))
    audio_err = validate_audio(audio, audio_duration)
    if audio_err:
        return JsonResponse({"error": audio_err}, status=400)
    if not content and not images and not audio:
        return JsonResponse({"error": "Message vide."}, status=400)
    reply_to = None
    rid = request.POST.get("reply_to")
    if rid:
        reply_to = DirectMessage.objects.filter(id=rid, conversation=conv).first()
    dm = _send_message(conv, request.user, is_admin=True, content=content, images=images,
                       reply_to=reply_to, audio=audio, audio_duration=audio_duration)
    return JsonResponse({"message": serialize_dm(_feed_qs(conv).get(id=dm.id), request)}, status=201)


# ── Indicateur "en train d'écrire" ──────────────────────────────────────────
@login_required
@require_POST
def support_typing(request):
    """Le client tape dans sa conversation support."""
    if request.user.is_staff:
        return JsonResponse({"ok": True})
    conv, _ = Conversation.objects.get_or_create(client=request.user)
    set_typing("conv", conv.id, request.user.id, _author_label(request.user), is_admin=False)
    return JsonResponse({"ok": True})


@staff_required
@require_POST
def inbox_typing(request, conv_id):
    """L'admin tape dans une conversation client."""
    conv = get_object_or_404(Conversation, id=conv_id)
    set_typing("conv", conv.id, request.user.id, "Équipe Hayiti's", is_admin=True)
    return JsonResponse({"ok": True})
