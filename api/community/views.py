from django.db.models import Prefetch
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ApiError
from api.permissions import IsAdminUser
from community import permissions as perm
from community.models import (
    Channel,
    ChannelSubscription,
    Message,
    MessageAttachment,
    MessageReaction,
    Notification,
)
from community.views import serialize_notification
from community.models import Conversation, DirectMessage
from community.support_views import _send_message
from community.views import (
    ALLOWED_IMAGE_TYPES,
    FEED_LIMIT,
    MAX_IMAGE_SIZE,
    MAX_IMAGES,
    REACTION_EMOJIS,
    _author_label,
)
from shop.models.Product import Product
from shop.templatetags.price_filters import _get_setting

from .serializers import ChannelSerializer, MessageSerializer

TAG = ["Communauté"]


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


class ChannelListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=TAG, summary="Liste des salons lisibles", responses=ChannelSerializer)
    def get(self, request):
        channels = perm.readable_channels(
            request.user, Channel.objects.filter(is_active=True)
        )
        data = ChannelSerializer(channels, many=True, context={"request": request}).data
        return Response({"success": True, "results": data})


class ChannelMessagesView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_channel(self, slug):
        try:
            return Channel.objects.get(slug=slug)
        except Channel.DoesNotExist:
            return None

    @extend_schema(
        tags=TAG,
        summary="Messages d'un salon (polling via after/before)",
        parameters=[
            OpenApiParameter("after", int, description="ID : messages plus récents"),
            OpenApiParameter("before", int, description="ID : messages plus anciens"),
        ],
        responses=MessageSerializer,
    )
    def get(self, request, slug):
        channel = self._get_channel(slug)
        if channel is None:
            raise ApiError("NOT_FOUND", "Salon introuvable.", status_code=404)
        if not perm.can_read_channel(request.user, channel):
            raise ApiError("PERMISSION_DENIED", "Salon inaccessible.")

        qs = _feed_queryset(channel)
        after = request.query_params.get("after")
        before = request.query_params.get("before")
        if after:
            msgs = list(qs.filter(id__gt=after).order_by("created_at")[:100])
        elif before:
            msgs = list(qs.filter(id__lt=before).order_by("-created_at")[:FEED_LIMIT])
            msgs.reverse()
        else:
            msgs = list(qs.order_by("-created_at")[:FEED_LIMIT])
            msgs.reverse()

        ctx = {"request": request, "setting": _get_setting()}
        data = MessageSerializer(msgs, many=True, context=ctx).data
        return Response({
            "success": True,
            "results": data,
            "last_id": data[-1]["id"] if data else (after or 0),
        })

    @extend_schema(tags=TAG, summary="Publier un message", responses=MessageSerializer)
    def post(self, request, slug):
        channel = self._get_channel(slug)
        if channel is None:
            raise ApiError("NOT_FOUND", "Salon introuvable.", status_code=404)
        if not perm.can_write_channel(request.user, channel):
            raise ApiError(
                "PERMISSION_DENIED",
                perm.write_block_reason(request.user, channel) or "Écriture interdite.",
            )

        content = (request.data.get("content") or "").strip()
        images = request.FILES.getlist("images")[:MAX_IMAGES]
        if not content and not images:
            raise ApiError("VALIDATION_ERROR", "Message vide.")
        if len(content) > 2000:
            raise ApiError("VALIDATION_ERROR", "Message trop long (2000 caractères max).")
        for f in images:
            if f.size == 0:
                raise ApiError("VALIDATION_ERROR", "Image vide (0 octet). Choisissez un fichier valide.")
            if f.size > MAX_IMAGE_SIZE:
                raise ApiError("VALIDATION_ERROR", "Image trop lourde (5 Mo max).")
            if f.content_type not in ALLOWED_IMAGE_TYPES:
                raise ApiError("VALIDATION_ERROR", "Format d'image non supporté.")

        product = None
        if request.data.get("product_id"):
            product = Product.objects.filter(id=request.data.get("product_id")).first()
        reply_to = None
        if request.data.get("reply_to"):
            reply_to = Message.objects.filter(
                id=request.data.get("reply_to"), channel=channel, is_deleted=False
            ).first()

        msg = Message.objects.create(
            channel=channel, author=request.user, content=content,
            product=product, reply_to=reply_to,
        )
        for f in images:
            MessageAttachment.objects.create(message=msg, image=f)

        msg = _feed_queryset(channel).get(id=msg.id)
        ctx = {"request": request, "setting": _get_setting()}
        return Response(
            {"success": True, "data": MessageSerializer(msg, context=ctx).data},
            status=status.HTTP_201_CREATED,
        )


class MessageReactView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=TAG, summary="Réagir à un message (toggle)")
    def post(self, request, pk):
        try:
            msg = Message.objects.get(pk=pk, is_deleted=False)
        except Message.DoesNotExist:
            raise ApiError("NOT_FOUND", "Message introuvable.", status_code=404)
        if not perm.can_read_channel(request.user, msg.channel):
            raise ApiError("PERMISSION_DENIED", "Salon inaccessible.")

        emoji = (request.data.get("emoji") or "❤️")[:8]
        if emoji not in REACTION_EMOJIS:
            raise ApiError("VALIDATION_ERROR", "Émoji non autorisé.")

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
        return Response({"success": True, "reactions": counts, "active": active, "emoji": emoji})


class MessageDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=TAG, summary="Supprimer son message (ou modération admin)")
    def delete(self, request, pk):
        try:
            msg = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise ApiError("NOT_FOUND", "Message introuvable.", status_code=404)
        if not (request.user.is_staff or msg.author_id == request.user.id):
            raise ApiError("PERMISSION_DENIED")
        msg.is_deleted = True
        msg.deleted_by = request.user
        msg.save(update_fields=["is_deleted", "deleted_by", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(tags=TAG, summary="Épingler/désépingler (admin)")
    def post(self, request, pk):
        if not request.user.is_staff:
            raise ApiError("PERMISSION_DENIED")
        try:
            msg = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise ApiError("NOT_FOUND", "Message introuvable.", status_code=404)
        msg.is_pinned = not msg.is_pinned
        msg.save(update_fields=["is_pinned", "updated_at"])
        return Response({"success": True, "is_pinned": msg.is_pinned})


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=TAG, summary="Mes notifications communauté + nombre de non-lus")
    def get(self, request):
        qs = Notification.objects.filter(recipient=request.user).select_related("actor", "channel")
        unread = qs.filter(is_read=False).count()
        results = [serialize_notification(n) for n in qs[:30]]
        return Response({"success": True, "unread": unread, "results": results})

    @extend_schema(tags=TAG, summary="Marquer les notifications comme lues")
    def post(self, request):
        qs = Notification.objects.filter(recipient=request.user, is_read=False)
        notif_id = request.data.get("id")
        if notif_id:
            qs = qs.filter(id=notif_id)
        marked = qs.update(is_read=True)
        return Response({"success": True, "marked": marked})


class ChannelSubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=TAG, summary="Suivre / ne plus suivre un salon (toggle)")
    def post(self, request, slug):
        try:
            channel = Channel.objects.get(slug=slug)
        except Channel.DoesNotExist:
            raise ApiError("NOT_FOUND", "Salon introuvable.", status_code=404)
        if not perm.can_read_channel(request.user, channel):
            raise ApiError("PERMISSION_DENIED", "Salon inaccessible.")
        sub = ChannelSubscription.objects.filter(channel=channel, user=request.user).first()
        if sub:
            sub.delete()
            following = False
        else:
            ChannelSubscription.objects.create(channel=channel, user=request.user)
            following = True
        return Response({"success": True, "following": following})


# ── Support privé (API) ─────────────────────────────────────────────────────
def _dm_payload(dm, request):
    return {
        "id": dm.id,
        "is_admin": dm.is_admin,
        "sender": "Équipe Hayiti's" if dm.is_admin else (_author_label(dm.sender) if dm.sender else "Client"),
        "content": dm.content,
        "attachments": [request.build_absolute_uri(a.image.url) for a in dm.attachments.all()],
        "created_at": dm.created_at.isoformat(),
        "is_own": bool(dm.sender_id == request.user.id),
    }


def _support_feed(request, conversation):
    qs = conversation.messages.select_related("sender").prefetch_related("attachments")
    after = request.query_params.get("after")
    before = request.query_params.get("before")
    if after:
        msgs = list(qs.filter(id__gt=after).order_by("created_at")[:100])
    elif before:
        msgs = list(qs.filter(id__lt=before).order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    else:
        msgs = list(qs.order_by("-created_at")[:FEED_LIMIT]); msgs.reverse()
    data = [_dm_payload(m, request) for m in msgs]
    return Response({"success": True, "results": data, "last_id": data[-1]["id"] if data else (after or 0)})


def _check_images(request):
    images = request.FILES.getlist("images")[:MAX_IMAGES]
    for f in images:
        if f.size == 0:
            raise ApiError("VALIDATION_ERROR", "Image vide (0 octet).")
        if f.size > MAX_IMAGE_SIZE:
            raise ApiError("VALIDATION_ERROR", "Image trop lourde (5 Mo max).")
        if f.content_type not in ALLOWED_IMAGE_TYPES:
            raise ApiError("VALIDATION_ERROR", "Format d'image non supporté.")
    return images


class SupportMessagesView(APIView):
    """Conversation support du client connecté."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=TAG, summary="Mes messages avec le support (polling)")
    def get(self, request):
        conv, _ = Conversation.objects.get_or_create(client=request.user)
        conv.messages.filter(is_admin=True, read_by_client=False).update(read_by_client=True)
        return _support_feed(request, conv)

    @extend_schema(tags=TAG, summary="Envoyer un message au support")
    def post(self, request):
        if request.user.is_staff:
            raise ApiError("VALIDATION_ERROR", "Les admins répondent via l'inbox.")
        conv, _ = Conversation.objects.get_or_create(client=request.user)
        content = (request.data.get("content") or "").strip()
        images = _check_images(request)
        if not content and not images:
            raise ApiError("VALIDATION_ERROR", "Message vide.")
        dm = _send_message(conv, request.user, is_admin=False, content=content, images=images)
        return Response({"success": True, "data": _dm_payload(dm, request)}, status=status.HTTP_201_CREATED)


class SupportInboxView(APIView):
    """Liste des conversations (admins)."""
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG, summary="Inbox support — liste des conversations (admin)")
    def get(self, request):
        from django.db.models import Count, Q
        convs = (
            Conversation.objects.select_related("client")
            .annotate(unread=Count("messages", filter=Q(messages__is_admin=False, messages__read_by_admin=False)))
            .filter(last_message_at__isnull=False)
        )
        results = []
        for c in convs:
            last = c.messages.order_by("-created_at").first()
            results.append({
                "id": c.id, "client": _author_label(c.client), "unread": c.unread,
                "last": (last.content[:60] if last and last.content else ("📷 image" if last else "")),
                "last_at": c.last_message_at.isoformat() if c.last_message_at else None,
            })
        return Response({"success": True, "results": results})


class SupportInboxMessagesView(APIView):
    """Messages d'une conversation côté admin."""
    permission_classes = [IsAdminUser]

    def _conv(self, conv_id):
        try:
            return Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            raise ApiError("NOT_FOUND", "Conversation introuvable.", status_code=404)

    @extend_schema(tags=TAG, summary="Messages d'une conversation (admin)")
    def get(self, request, conv_id):
        conv = self._conv(conv_id)
        conv.messages.filter(is_admin=False, read_by_admin=False).update(read_by_admin=True)
        return _support_feed(request, conv)

    @extend_schema(tags=TAG, summary="Répondre à un client (admin)")
    def post(self, request, conv_id):
        conv = self._conv(conv_id)
        content = (request.data.get("content") or "").strip()
        images = _check_images(request)
        if not content and not images:
            raise ApiError("VALIDATION_ERROR", "Message vide.")
        dm = _send_message(conv, request.user, is_admin=True, content=content, images=images)
        return Response({"success": True, "data": _dm_payload(dm, request)}, status=status.HTTP_201_CREATED)
