from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from shop.models import Product
from shop.templatetags.price_filters import _format, _get_rate, _get_setting

from . import permissions as perm
from .models import Channel, Message, MessageAttachment, MessageReaction

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

    context = {
        "channels": channels,
        "active_channel": active,
        "initial_messages": initial,
        "can_write": perm.can_write_channel(request.user, active),
        "block_reason": perm.write_block_reason(request.user, active),
        "reaction_emojis": REACTION_EMOJIS,
        "last_id": initial[-1]["id"] if initial else 0,
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
