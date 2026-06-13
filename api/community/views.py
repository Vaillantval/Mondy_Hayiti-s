from django.db.models import Prefetch
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ApiError
from community import permissions as perm
from community.models import (
    Channel,
    Message,
    MessageAttachment,
    MessageReaction,
)
from community.views import (
    ALLOWED_IMAGE_TYPES,
    FEED_LIMIT,
    MAX_IMAGE_SIZE,
    MAX_IMAGES,
    REACTION_EMOJIS,
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
