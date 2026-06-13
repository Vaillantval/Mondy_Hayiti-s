from django.conf import settings
from django.db import models
from django.utils.text import slugify

from shop.models.Product import Product

User = settings.AUTH_USER_MODEL


class Channel(models.Model):
    """Salon thématique de la communauté (type 'groupe WhatsApp / Discord')."""

    READ_PUBLIC = "public"
    READ_AUTH = "authenticated"
    READ_CLOSED = "closed"
    READ_CHOICES = [
        (READ_PUBLIC, "Public — tout le monde peut lire"),
        (READ_AUTH, "Connectés uniquement"),
        (READ_CLOSED, "Fermé — admins uniquement"),
    ]

    WRITE_OPEN = "open"
    WRITE_LOCKED = "locked"
    WRITE_ADMINS = "admins"
    WRITE_CHOICES = [
        (WRITE_OPEN, "Ouvert — membres connectés"),
        (WRITE_LOCKED, "Verrouillé — lecture seule"),
        (WRITE_ADMINS, "Admins uniquement"),
    ]

    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    description = models.CharField(max_length=160, blank=True, default="")
    emoji = models.CharField(
        max_length=8, default="💬", help_text="Émoji affiché à côté du nom du salon."
    )
    color = models.CharField(
        max_length=7, default="#C62828", help_text="Couleur d'accent (hex)."
    )
    image = models.ImageField(
        upload_to="community/channels/%Y/%m/%d/", blank=True, null=True
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    read_access = models.CharField(
        max_length=20, choices=READ_CHOICES, default=READ_PUBLIC,
        verbose_name="Accès en lecture",
    )
    write_access = models.CharField(
        max_length=20, choices=WRITE_CHOICES, default=WRITE_OPEN,
        verbose_name="Accès en écriture",
    )
    notify_admins = models.BooleanField(
        default=True,
        help_text="Notifier les admins (push FCM) à chaque nouveau message de membre.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Salon"
        verbose_name_plural = "Salons"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "salon"
            slug = base
            n = 1
            while Channel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Message(models.Model):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="messages"
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="community_messages",
    )
    content = models.TextField(blank=True, default="")
    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="replies",
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="community_mentions",
        help_text="Produit tagué dans le message.",
    )
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["channel", "created_at"]),
        ]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        who = self.author.username if self.author else "—"
        return f"[{self.channel.slug}] {who}: {self.content[:40]}"


class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="attachments"
    )
    image = models.ImageField(upload_to="community/attachments/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment #{self.id} (message {self.message_id})"


class MessageReaction(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="reactions"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="community_reactions"
    )
    emoji = models.CharField(max_length=8, default="❤️")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "user", "emoji")
        verbose_name = "Réaction"
        verbose_name_plural = "Réactions"

    def __str__(self):
        return f"{self.emoji} by {self.user_id} on {self.message_id}"


class CommunityBan(models.Model):
    """Blocage global d'un utilisateur sur toute la communauté."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="community_ban"
    )
    reason = models.CharField(max_length=255, blank=True, default="")
    can_read = models.BooleanField(
        default=True,
        help_text="Si décoché, l'utilisateur ne peut plus rien lire non plus.",
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bannissement"
        verbose_name_plural = "Bannissements"

    def __str__(self):
        return f"Ban {self.user_id} ({'actif' if self.is_active else 'inactif'})"


class ChannelMute(models.Model):
    """Empêche un utilisateur précis d'écrire dans un salon précis."""

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="mutes"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channel_mutes"
    )
    reason = models.CharField(max_length=255, blank=True, default="")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("channel", "user")
        verbose_name = "Mute (salon)"
        verbose_name_plural = "Mutes (salon)"

    def __str__(self):
        return f"Mute {self.user_id} on {self.channel.slug}"
