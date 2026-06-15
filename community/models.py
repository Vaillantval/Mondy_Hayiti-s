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
    audio = models.FileField(
        upload_to="community/audio/%Y/%m/%d/", blank=True, null=True,
        help_text="Note vocale.",
    )
    audio_duration = models.PositiveIntegerField(default=0, help_text="Durée de la note vocale (s).")
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


class ChannelSubscription(models.Model):
    """Un membre suit un salon → reçoit une notif aux nouveaux messages.

    Créée automatiquement quand l'utilisateur poste dans un salon, et pilotable
    via un bouton « Suivre / Ne plus suivre ». `muted` coupe les notifs sans
    perdre l'abonnement.
    """

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="subscriptions"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channel_subscriptions"
    )
    muted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("channel", "user")
        verbose_name = "Abonnement salon"
        verbose_name_plural = "Abonnements salon"

    def __str__(self):
        return f"{self.user_id} suit {self.channel.slug}"


class ChannelRead(models.Model):
    """Curseur de lecture d'un utilisateur dans un salon (pour les accusés « vu par »).

    `last_read_id` = id du dernier message vu. Un utilisateur a « lu » un message X
    si son `last_read_id >= X.id`.
    """

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="reads"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channel_reads"
    )
    last_read_id = models.PositiveBigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("channel", "user")
        verbose_name = "Lecture salon"
        verbose_name_plural = "Lectures salon"

    def __str__(self):
        return f"{self.user_id} a lu {self.channel.slug} jusqu'à {self.last_read_id}"


class Notification(models.Model):
    """Notification in-app (et trace de ce qui a été poussé en push)."""

    TYPE_REPLY = "reply"
    TYPE_MENTION = "mention"
    TYPE_CHANNEL = "channel_message"
    TYPE_SUPPORT = "support"
    TYPE_CHOICES = [
        (TYPE_REPLY, "Réponse à votre message"),
        (TYPE_MENTION, "Mention"),
        (TYPE_CHANNEL, "Nouveau message dans un salon suivi"),
        (TYPE_SUPPORT, "Message du support"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="community_notifications"
    )
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    count = models.PositiveIntegerField(default=1)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
        ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"[{self.type}] → {self.recipient_id} (lu={self.is_read})"


class WebPushToken(models.Model):
    """Jeton d'enregistrement Web Push (Firebase Web) pour un navigateur."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="web_push_tokens"
    )
    token = models.CharField(max_length=512, unique=True)
    user_agent = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jeton Web Push"
        verbose_name_plural = "Jetons Web Push"

    def __str__(self):
        return f"WebPush {self.user_id} ({self.token[:12]}…)"


class Conversation(models.Model):
    """Fil de support privé entre un client et l'équipe admin (inbox partagée).

    Un seul fil par client : n'importe quel admin le voit et y répond au nom de
    l'équipe.
    """

    client = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="support_conversation"
    )
    is_archived = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_message_at", "-created_at"]
        verbose_name = "Conversation support"
        verbose_name_plural = "Conversations support"

    def __str__(self):
        return f"Support · {self.client.username}"


class DirectMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="support_messages",
    )
    is_admin = models.BooleanField(
        default=False, help_text="Message envoyé par l'équipe (admin) plutôt que le client."
    )
    content = models.TextField(blank=True, default="")
    audio = models.FileField(
        upload_to="community/support/audio/%Y/%m/%d/", blank=True, null=True,
        help_text="Note vocale.",
    )
    audio_duration = models.PositiveIntegerField(default=0)
    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies"
    )
    read_by_client = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["conversation", "created_at"])]
        verbose_name = "Message support"
        verbose_name_plural = "Messages support"

    def __str__(self):
        who = "Équipe" if self.is_admin else "Client"
        return f"[{self.conversation_id}] {who}: {self.content[:30]}"


class DirectMessageAttachment(models.Model):
    message = models.ForeignKey(
        DirectMessage, on_delete=models.CASCADE, related_name="attachments"
    )
    image = models.ImageField(upload_to="community/support/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SupportAttachment #{self.id} (message {self.message_id})"
