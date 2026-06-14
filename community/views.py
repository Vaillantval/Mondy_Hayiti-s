import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from shop.models import Product
from shop.templatetags.price_filters import _format, _get_rate, _get_setting

from . import permissions as perm
from .models import (
    Channel,
    ChannelMute,
    ChannelSubscription,
    CommunityBan,
    Message,
    MessageAttachment,
    MessageReaction,
    Notification,
    WebPushToken,
)

# ── Limites upload ──────────────────────────────────────────────────────────
MAX_IMAGES = 4
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 Mo
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
REACTION_EMOJIS = ["❤️", "😋", "🔥", "👍", "🎂", "😮"]
FEED_LIMIT = 30


# ── Helpers de sérialisation ────────────────────────────────────────────────
def _product_payload(product, setting):
    if not product:
        return None
    img = product.images.first()
    price = product.solde_price or product.regular_price
    if setting:
        rate = _get_rate(setting.base_currency, setting.currency)
        price_display = _format(price * rate, setting.currency)
    else:
        price_display = f"{price:.2f}"
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "image": img.image.url if img else None,
        "price": price_display,
    }


def _author_label(author):
    if not author:
        return "Membre supprimé"
    full = f"{author.first_name} {author.last_name}".strip()
    return full or author.username


def serialize_message(msg, request, setting):
    user = request.user
    is_own = bool(user.is_authenticated and msg.author_id == user.id)
    can_moderate = bool(user.is_authenticated and user.is_staff)

    # Réactions agrégées par émoji + celles de l'utilisateur courant
    counts, mine = {}, []
    for r in msg.reactions.all():
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
        if user.is_authenticated and r.user_id == user.id:
            mine.append(r.emoji)

    reply = None
    if msg.reply_to and not msg.reply_to.is_deleted:
        reply = {
            "id": msg.reply_to.id,
            "author": _author_label(msg.reply_to.author),
            "excerpt": (msg.reply_to.content[:80] or "📷 image"),
        }

    if msg.is_deleted:
        return {
            "id": msg.id,
            "deleted": True,
            "content": "Message supprimé par la modération.",
            "is_own": is_own,
            "can_moderate": can_moderate,
        }

    return {
        "id": msg.id,
        "deleted": False,
        "author": _author_label(msg.author),
        "author_id": msg.author_id,
        "is_staff": bool(msg.author and msg.author.is_staff),
        "initial": (_author_label(msg.author)[:1] or "?").upper(),
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
        "is_pinned": msg.is_pinned,
        "is_own": is_own,
        "can_moderate": can_moderate,
        "product": _product_payload(msg.product, setting),
        "reply_to": reply,
        "attachments": [a.image.url for a in msg.attachments.all()],
        "reactions": counts,
        "my_reactions": mine,
    }


def _feed_queryset(channel):
    return (
        Message.objects.filter(channel=channel)
        .select_related("author", "product", "reply_to", "reply_to__author")
        .prefetch_related(
            "reactions",
            Prefetch("attachments", queryset=MessageAttachment.objects.order_by("id")),
            Prefetch("product__images"),
        )
    )


# ── Pages ───────────────────────────────────────────────────────────────────
def community_home(request, slug=None):
    channels_qs = Channel.objects.filter(is_active=True)
    channels = perm.readable_channels(request.user, channels_qs)

    if not channels:
        return render(request, "community/community.html", {
            "channels": [], "active_channel": None, "no_access": True,
        })

    if slug:
        active = next((c for c in channels if c.slug == slug), None)
        if active is None:
            return redirect("community:home")
    else:
        active = channels[0]

    setting = _get_setting()
    msgs = list(_feed_queryset(active).order_by("-created_at")[:FEED_LIMIT])
    msgs.reverse()
    initial = [serialize_message(m, request, setting) for m in msgs]

    is_following = (
        request.user.is_authenticated
        and ChannelSubscription.objects.filter(channel=active, user=request.user).exists()
    )
    context = {
        "channels": channels,
        "active_channel": active,
        "initial_messages": initial,
        "can_write": perm.can_write_channel(request.user, active),
        "block_reason": perm.write_block_reason(request.user, active),
        "reaction_emojis": REACTION_EMOJIS,
        "last_id": initial[-1]["id"] if initial else 0,
        "is_following": is_following,
    }
    return render(request, "community/community.html", context)


# ── Endpoints JSON ──────────────────────────────────────────────────────────
@require_GET
def messages_feed(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    if not perm.can_read_channel(request.user, channel):
        return JsonResponse({"error": "forbidden"}, status=403)

    setting = _get_setting()
    qs = _feed_queryset(channel)

    after = request.GET.get("after")
    before = request.GET.get("before")
    if after:
        msgs = list(qs.filter(id__gt=after).order_by("created_at")[:100])
    elif before:
        msgs = list(qs.filter(id__lt=before).order_by("-created_at")[:FEED_LIMIT])
        msgs.reverse()
    else:
        msgs = list(qs.order_by("-created_at")[:FEED_LIMIT])
        msgs.reverse()

    data = [serialize_message(m, request, setting) for m in msgs]
    return JsonResponse({
        "messages": data,
        "last_id": data[-1]["id"] if data else (after or 0),
        "has_more": len(msgs) >= FEED_LIMIT if before is not None or not after else False,
    })


@login_required
@require_POST
def post_message(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    if not perm.can_write_channel(request.user, channel):
        return JsonResponse(
            {"error": perm.write_block_reason(request.user, channel) or "forbidden"},
            status=403,
        )

    content = (request.POST.get("content") or "").strip()
    images = request.FILES.getlist("images")[:MAX_IMAGES]

    if not content and not images:
        return JsonResponse({"error": "Message vide."}, status=400)
    if len(content) > 2000:
        return JsonResponse({"error": "Message trop long (2000 caractères max)."}, status=400)

    for f in images:
        if f.size == 0:
            return JsonResponse({"error": "Image vide (0 octet). Choisissez un fichier valide."}, status=400)
        if f.size > MAX_IMAGE_SIZE:
            return JsonResponse({"error": "Image trop lourde (5 Mo max)."}, status=400)
        if f.content_type not in ALLOWED_IMAGE_TYPES:
            return JsonResponse({"error": "Format d'image non supporté."}, status=400)

    product = None
    product_id = request.POST.get("product_id")
    if product_id:
        product = Product.objects.filter(id=product_id).first()

    reply_to = None
    reply_id = request.POST.get("reply_to")
    if reply_id:
        reply_to = Message.objects.filter(id=reply_id, channel=channel, is_deleted=False).first()

    msg = Message.objects.create(
        channel=channel, author=request.user, content=content,
        product=product, reply_to=reply_to,
    )
    for f in images:
        MessageAttachment.objects.create(message=msg, image=f)

    setting = _get_setting()
    msg = _feed_queryset(channel).get(id=msg.id)
    return JsonResponse({"message": serialize_message(msg, request, setting)}, status=201)


@login_required
@require_POST
def react_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, is_deleted=False)
    if not perm.can_read_channel(request.user, msg.channel):
        return JsonResponse({"error": "forbidden"}, status=403)

    emoji = (request.POST.get("emoji") or "❤️")[:8]
    if emoji not in REACTION_EMOJIS:
        return JsonResponse({"error": "Émoji non autorisé."}, status=400)

    existing = MessageReaction.objects.filter(message=msg, user=request.user, emoji=emoji).first()
    if existing:
        existing.delete()
        active = False
    else:
        MessageReaction.objects.create(message=msg, user=request.user, emoji=emoji)
        active = True

    counts = {}
    for r in msg.reactions.all():
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
    return JsonResponse({"reactions": counts, "active": active, "emoji": emoji})


@login_required
@require_POST
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    if not (request.user.is_staff or msg.author_id == request.user.id):
        return JsonResponse({"error": "forbidden"}, status=403)
    msg.is_deleted = True
    msg.deleted_by = request.user
    msg.save(update_fields=["is_deleted", "deleted_by", "updated_at"])
    return JsonResponse({"ok": True})


@login_required
@require_POST
def pin_message(request, message_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)
    msg = get_object_or_404(Message, id=message_id)
    msg.is_pinned = not msg.is_pinned
    msg.save(update_fields=["is_pinned", "updated_at"])
    return JsonResponse({"ok": True, "is_pinned": msg.is_pinned})


@login_required
@require_GET
def product_search(request):
    q = (request.GET.get("q") or "").strip()
    qs = Product.objects.filter(is_available=True)
    if q:
        qs = qs.filter(name__icontains=q)
    setting = _get_setting()
    results = [_product_payload(p, setting) for p in qs.prefetch_related("images")[:8]]
    return JsonResponse({"results": results})


# ── Notifications ───────────────────────────────────────────────────────────
def serialize_notification(n):
    actor = _author_label(n.actor) if n.actor else "Quelqu'un"
    emoji = n.channel.emoji if n.channel else "🔔"
    url = f"/community/c/{n.channel.slug}/" if n.channel else "/community/"

    if n.type == Notification.TYPE_REPLY:
        text = f"{actor} a répondu à votre message"
    elif n.type == Notification.TYPE_MENTION:
        text = f"{actor} vous a mentionné"
    elif n.type == Notification.TYPE_SUPPORT:
        emoji = "📨"
        if n.recipient.is_staff:
            text = f"{actor} vous a écrit (support)"
            url = f"/community/inbox/{n.conversation_id}/" if n.conversation_id else "/community/inbox/"
        else:
            text = "L'équipe Hayiti's vous a répondu"
            url = "/community/support/"
    else:
        plural = "s" if n.count > 1 else ""
        text = f"{n.count} nouveau{plural} message{plural} dans {n.channel.name if n.channel else 'un salon'}"
    return {
        "id": n.id,
        "type": n.type,
        "text": text,
        "message": text,           # alias attendu par l'app mobile
        "actor_name": actor,       # nom de l'acteur (sous-titre mobile)
        "channel": n.channel.slug if n.channel else None,
        "channel_name": n.channel.name if n.channel else None,
        "emoji": emoji,
        "count": n.count,
        "is_read": n.is_read,
        "url": url,
        "created_at": n.updated_at.isoformat(),
    }


@login_required
@require_GET
def notifications_feed(request):
    qs = Notification.objects.filter(recipient=request.user).select_related("actor", "channel")
    unread = qs.filter(is_read=False).count()
    results = [serialize_notification(n) for n in qs[:20]]
    return JsonResponse({"unread": unread, "results": results})


@login_required
@require_POST
def notifications_read(request):
    qs = Notification.objects.filter(recipient=request.user, is_read=False)
    notif_id = request.POST.get("id")
    if notif_id:
        qs = qs.filter(id=notif_id)
    updated = qs.update(is_read=True)
    return JsonResponse({"ok": True, "marked": updated})


@login_required
@require_POST
def channel_subscribe(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    if not perm.can_read_channel(request.user, channel):
        return JsonResponse({"error": "forbidden"}, status=403)
    sub = ChannelSubscription.objects.filter(channel=channel, user=request.user).first()
    if sub:
        sub.delete()
        following = False
    else:
        ChannelSubscription.objects.create(channel=channel, user=request.user)
        following = True
    return JsonResponse({"ok": True, "following": following})


@login_required
@require_POST
def push_subscribe(request):
    token = (request.POST.get("token") or "").strip()
    if not token:
        return JsonResponse({"error": "token manquant"}, status=400)
    WebPushToken.objects.update_or_create(
        token=token,
        defaults={"user": request.user, "user_agent": request.META.get("HTTP_USER_AGENT", "")[:255]},
    )
    return JsonResponse({"ok": True})


@login_required
@require_POST
def push_unsubscribe(request):
    token = (request.POST.get("token") or "").strip()
    if token:
        WebPushToken.objects.filter(token=token, user=request.user).delete()
    return JsonResponse({"ok": True})


# ── Modération in-UI (staff) ────────────────────────────────────────────────
@login_required
@require_POST
def ban_author(request, message_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)
    msg = get_object_or_404(Message, id=message_id)
    if not msg.author_id or msg.author.is_staff:
        return JsonResponse({"error": "Action impossible sur cet utilisateur."}, status=400)
    ban, created = CommunityBan.objects.get_or_create(
        user=msg.author,
        defaults={"is_active": True, "created_by": request.user, "reason": "Banni depuis la communauté"},
    )
    if not created:
        ban.is_active = not ban.is_active
        ban.save(update_fields=["is_active"])
    return JsonResponse({"ok": True, "banned": ban.is_active, "user": msg.author.username})


@login_required
@require_POST
def mute_author(request, message_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)
    msg = get_object_or_404(Message, id=message_id)
    if not msg.author_id or msg.author.is_staff:
        return JsonResponse({"error": "Action impossible sur cet utilisateur."}, status=400)
    mute = ChannelMute.objects.filter(channel=msg.channel, user=msg.author).first()
    if mute:
        mute.delete()
        muted = False
    else:
        ChannelMute.objects.create(channel=msg.channel, user=msg.author, created_by=request.user)
        muted = True
    return JsonResponse({"ok": True, "muted": muted, "user": msg.author.username})


@login_required
@require_POST
def lock_channel(request, slug):
    if not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)
    ch = get_object_or_404(Channel, slug=slug)
    order = [Channel.WRITE_OPEN, Channel.WRITE_LOCKED, Channel.WRITE_ADMINS]
    i = order.index(ch.write_access) if ch.write_access in order else 0
    ch.write_access = order[(i + 1) % len(order)]
    ch.save(update_fields=["write_access", "updated_at"])
    return JsonResponse({"ok": True, "write_access": ch.write_access, "label": ch.get_write_access_display()})


@login_required
def manage_channels(request):
    if not request.user.is_staff:
        return redirect("community:home")
    return render(request, "community/manage_channels.html", {
        "channels": Channel.objects.all(),
        "read_choices": Channel.READ_CHOICES,
        "write_choices": Channel.WRITE_CHOICES,
    })


@login_required
@require_POST
def channel_save(request):
    if not request.user.is_staff:
        return redirect("community:home")
    name = (request.POST.get("name") or "").strip()
    if not name:
        return redirect("community:manage_channels")
    read_vals = {c[0] for c in Channel.READ_CHOICES}
    write_vals = {c[0] for c in Channel.WRITE_CHOICES}
    fields = {
        "name": name,
        "emoji": (request.POST.get("emoji") or "💬")[:8],
        "description": (request.POST.get("description") or "")[:160],
        "read_access": request.POST.get("read_access") if request.POST.get("read_access") in read_vals else Channel.READ_PUBLIC,
        "write_access": request.POST.get("write_access") if request.POST.get("write_access") in write_vals else Channel.WRITE_OPEN,
        "is_active": request.POST.get("is_active") == "1",
    }
    cid = request.POST.get("id")
    if cid:
        Channel.objects.filter(id=cid).update(**fields)
    else:
        Channel.objects.create(**fields)
    return redirect("community:manage_channels")


@require_GET
def firebase_messaging_sw(request):
    """Service Worker Firebase, servi à la racine pour couvrir tout le site."""
    cfg = json.dumps(getattr(settings, "FIREBASE_WEB_CONFIG", {}))
    js = (
        "importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');\n"
        "importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');\n"
        "try {\n"
        f"  firebase.initializeApp({cfg});\n"
        "  const messaging = firebase.messaging();\n"
        "  messaging.onBackgroundMessage(function (payload) {\n"
        "    const n = payload.notification || {};\n"
        "    self.registration.showNotification(n.title || \"Hayiti's\", {\n"
        "      body: n.body || '', data: payload.data || {}, badge: '/static/favicon.png'\n"
        "    });\n"
        "  });\n"
        "} catch (e) {}\n"
        "self.addEventListener('notificationclick', function (event) {\n"
        "  event.notification.close();\n"
        "  const d = event.notification.data || {};\n"
        "  const url = d.channel ? '/community/c/' + d.channel + '/' : '/community/';\n"
        "  event.waitUntil(clients.openWindow(url));\n"
        "});\n"
    )
    resp = HttpResponse(js, content_type="application/javascript")
    resp["Service-Worker-Allowed"] = "/"
    return resp
