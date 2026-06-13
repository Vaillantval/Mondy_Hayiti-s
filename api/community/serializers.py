from rest_framework import serializers

from community.models import Channel, Message
from shop.templatetags.price_filters import _format, _get_rate, _get_setting


def _abs(request, url):
    if not url:
        return None
    return request.build_absolute_uri(url) if request else url


class ChannelSerializer(serializers.ModelSerializer):
    can_write = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            "id", "name", "slug", "description", "emoji", "color", "image",
            "read_access", "write_access", "can_write",
        ]

    def get_image(self, obj):
        return _abs(self.context.get("request"), obj.image.url) if obj.image else None

    def get_can_write(self, obj):
        from community import permissions as perm
        request = self.context.get("request")
        return perm.can_write_channel(request.user, obj) if request else False


class MessageSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    my_reactions = serializers.SerializerMethodField()
    is_own = serializers.SerializerMethodField()
    can_moderate = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "channel", "author", "author_name", "is_staff", "content",
            "created_at", "is_pinned", "is_deleted", "product", "reply_to",
            "attachments", "reactions", "my_reactions", "is_own", "can_moderate",
        ]

    def _label(self, author):
        if not author:
            return "Membre supprimé"
        full = f"{author.first_name} {author.last_name}".strip()
        return full or author.username

    def get_author_name(self, obj):
        if obj.is_deleted:
            return None
        return self._label(obj.author)

    def get_is_staff(self, obj):
        return bool(obj.author and obj.author.is_staff)

    def get_is_own(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and obj.author_id == request.user.id)

    def get_can_moderate(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user.is_staff)

    def get_product(self, obj):
        if obj.is_deleted or not obj.product:
            return None
        request = self.context.get("request")
        setting = self.context.get("setting") or _get_setting()
        p = obj.product
        img = p.images.first()
        price = p.solde_price or p.regular_price
        if setting:
            price = price * _get_rate(setting.base_currency, setting.currency)
            price_display = _format(price, setting.currency)
        else:
            price_display = f"{price:.2f}"
        return {
            "id": p.id, "name": p.name, "slug": p.slug,
            "image": _abs(request, img.image.url) if img else None,
            "price": price_display,
        }

    def get_reply_to(self, obj):
        if not obj.reply_to or obj.reply_to.is_deleted:
            return None
        r = obj.reply_to
        return {"id": r.id, "author": self._label(r.author), "excerpt": (r.content[:80] or "📷 image")}

    def get_attachments(self, obj):
        if obj.is_deleted:
            return []
        request = self.context.get("request")
        return [_abs(request, a.image.url) for a in obj.attachments.all()]

    def get_reactions(self, obj):
        counts = {}
        for r in obj.reactions.all():
            counts[r.emoji] = counts.get(r.emoji, 0) + 1
        return counts

    def get_my_reactions(self, obj):
        request = self.context.get("request")
        if not (request and request.user.is_authenticated):
            return []
        return [r.emoji for r in obj.reactions.all() if r.user_id == request.user.id]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        if obj.is_deleted:
            data["content"] = "Message supprimé par la modération."
        return data
