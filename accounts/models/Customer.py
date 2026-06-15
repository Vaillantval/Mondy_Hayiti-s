from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    agree_terms = models.BooleanField(default=False)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fcm_token = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Firebase Cloud Messaging token pour les push notifications Flutter.",
    )
    read_receipts = models.BooleanField(
        default=True,
        help_text="Si désactivé, l'utilisateur n'envoie plus d'accusés de lecture "
                  "(personne ne voit quand il a lu un message).",
    )