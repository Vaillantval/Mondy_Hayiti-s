"""Notifications best-effort vers les admins à chaque nouveau message de membre."""
import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def notify_admins_on_new_message(sender, instance, created, **kwargs):
    if not created or instance.is_deleted:
        return
    author = instance.author
    if author is None or author.is_staff:
        return
    channel = instance.channel
    if not channel.notify_admins:
        return

    transaction.on_commit(lambda: _push_to_admins(instance))


def _push_to_admins(message):
    try:
        from notifications.fcm import send_to_token
    except Exception:  # Firebase non configuré → on ignore silencieusement.
        return

    User = get_user_model()
    staff_tokens = (
        User.objects.filter(is_staff=True, is_active=True)
        .exclude(fcm_token__isnull=True)
        .exclude(fcm_token="")
        .values_list("fcm_token", flat=True)
    )
    author_name = message.author.username if message.author else "Un visiteur"
    title = f"💬 {message.channel.name}"
    body = f"{author_name} : {message.content[:80]}" if message.content else f"{author_name} a partagé une image."
    data = {"type": "community_message", "channel": message.channel.slug, "message_id": str(message.id)}

    for token in staff_tokens:
        try:
            send_to_token(token, title, body, data)
        except Exception as exc:
            logger.warning("Échec notif FCM admin: %s", exc)
