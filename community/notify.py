"""Création des notifications communauté + livraison push (mobile + web).

Tout est best-effort : si Firebase n'est pas configuré, les push sont ignorés
silencieusement (les notifications in-app, elles, sont toujours créées).
"""
import logging
import re

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q

from . import permissions as perm
from .models import ChannelSubscription, Notification, WebPushToken

logger = logging.getLogger(__name__)
User = get_user_model()

# @pseudo — autorise les caractères d'username Django (lettres, chiffres, @ . + - _)
MENTION_RE = re.compile(r"@([\w.@+\-]+)")
PUSH_THROTTLE_SECONDS = 300  # 1 push « nouveau message » max / salon / utilisateur / 5 min


def extract_mention_usernames(content):
    return {m.strip(".").lower() for m in MENTION_RE.findall(content or "") if m}


def _name(u):
    full = f"{u.first_name} {u.last_name}".strip()
    return full or u.username


def collect_tokens(user):
    """Tous les jetons push d'un utilisateur : mobile (fcm_token) + web."""
    tokens = []
    mobile = getattr(user, "fcm_token", None)
    if mobile:
        tokens.append(mobile)
    tokens += list(user.web_push_tokens.values_list("token", flat=True))
    return tokens


def push_to_user(user, title, body, data=None):
    try:
        from notifications.fcm import send_to_token
    except Exception:
        return
    for tok in collect_tokens(user):
        try:
            send_to_token(tok, title, body, data or {})
        except Exception as exc:
            logger.warning("Push échec (token ignoré) : %s", exc)


def _create(recipient, actor, ntype, channel, message, coalesce=False):
    """Crée une notification in-app, ou regroupe l'existante non lue (coalesce)."""
    if actor and recipient.id == actor.id:
        return None
    if coalesce:
        notif, created = Notification.objects.get_or_create(
            recipient=recipient, channel=channel, type=ntype, is_read=False,
            defaults={"actor": actor, "message": message},
        )
        if not created:
            notif.count += 1
            notif.actor = actor
            notif.message = message
            notif.save(update_fields=["count", "actor", "message", "updated_at"])
        return notif
    return Notification.objects.create(
        recipient=recipient, actor=actor, type=ntype, channel=channel, message=message
    )


def notify_for_message(message):
    """Point d'entrée appelé à la création d'un message (via signal, on_commit)."""
    channel = message.channel
    author = message.author
    if author is None:
        return

    # L'auteur suit désormais ce salon (pour être notifié des suites).
    ChannelSubscription.objects.get_or_create(channel=channel, user=author)

    actor_name = _name(author)
    excerpt = (message.content[:80] or "📷 image")
    notified = {author.id}  # évite doublons et auto-notification

    # 1) Réponse à un message
    rt = message.reply_to
    if rt and rt.author_id and rt.author_id not in notified:
        target = rt.author
        if _create(target, author, Notification.TYPE_REPLY, channel, message):
            notified.add(target.id)
            push_to_user(
                target, f"💬 {actor_name} a répondu", excerpt,
                {"type": "reply", "channel": channel.slug, "message_id": str(message.id)},
            )

    # 2) Mentions @pseudo
    usernames = extract_mention_usernames(message.content)
    if usernames:
        q = Q()
        for un in usernames:
            q |= Q(username__iexact=un)
        for u in User.objects.filter(q):
            if u.id in notified or not perm.can_read_channel(u, channel):
                continue
            if _create(u, author, Notification.TYPE_MENTION, channel, message):
                notified.add(u.id)
                push_to_user(
                    u, f"📣 {actor_name} vous a mentionné", excerpt,
                    {"type": "mention", "channel": channel.slug, "message_id": str(message.id)},
                )

    # 3) Abonnés du salon (nouveau message), avec throttling du push
    subs = (
        ChannelSubscription.objects.filter(channel=channel, muted=False)
        .exclude(user_id__in=notified)
        .select_related("user")
    )
    for sub in subs:
        u = sub.user
        if u.id in notified or not perm.can_read_channel(u, channel):
            continue
        if _create(u, author, Notification.TYPE_CHANNEL, channel, message, coalesce=True):
            notified.add(u.id)
            ck = f"cmpush:{u.id}:{channel.id}"
            if not cache.get(ck):
                cache.set(ck, 1, PUSH_THROTTLE_SECONDS)
                push_to_user(
                    u, f"💬 {channel.name}", f"{actor_name} : {excerpt}",
                    {"type": "channel_message", "channel": channel.slug, "message_id": str(message.id)},
                )

    # 4) Alerte admins (push only — conserve le comportement existant)
    if channel.notify_admins and not author.is_staff:
        staff = User.objects.filter(is_staff=True, is_active=True).exclude(id__in=notified)
        for u in staff:
            push_to_user(
                u, f"💬 {channel.name}", f"{actor_name} : {excerpt}",
                {"type": "community_message", "channel": channel.slug, "message_id": str(message.id)},
            )
