"""Déclenche la création/diffusion des notifications à chaque nouveau message."""
import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def on_new_message(sender, instance, created, **kwargs):
    if not created or instance.is_deleted or instance.author_id is None:
        return

    def _run():
        try:
            from .notify import notify_for_message
            notify_for_message(instance)
        except Exception as exc:  # ne jamais casser la requête de post
            logger.warning("notify_for_message a échoué : %s", exc)

    transaction.on_commit(_run)
