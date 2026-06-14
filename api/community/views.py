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
    ChannelMute,
    ChannelSubscription,
    CommunityBan,
    Conversation,
    DirectMessage,
    Message,
    MessageAttachment,
    MessageReaction,
    Notification,
)
from community.views import serialize_notification
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

from .serializers import ChannelAdminSerializer, ChannelSerializer, MessageSerializer

TAG = ["Communauté"]
TAG_MOD = ["Communauté · modération"]


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
def _dm_label(dm):
    return "Équipe Hayiti's" if dm.is_admin else (_author_label(dm.sender) if dm.sender else "Client")


def _dm_payload(dm, request):
    reply = None
    if dm.reply_to_id and dm.reply_to:
        rt = dm.reply_to
        reply = {"id": rt.id, "sender": _dm_label(rt), "excerpt": (rt.content[:80] or "📷 image")}
    return {
        "id": dm.id,
        "is_admin": dm.is_admin,
        "sender": _dm_label(dm),
        "content": dm.content,
        "reply_to": reply,
        "attachments": [request.build_absolute_uri(a.image.url) for a in dm.attachments.all()],
        "created_at": dm.created_at.isoformat(),
        "is_own": bool(dm.sender_id == request.user.id),
    }


def _resolve_dm_reply(request, conversation):
    rid = request.data.get("reply_to")
    if rid:
        return DirectMessage.objects.filter(id=rid, conversation=conversation).first()
    return None


def _support_feed(request, conversation):
    qs = conversation.messages.select_related("sender", "reply_to", "reply_to__sender").prefetch_related("attachments")
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
        dm = _send_message(conv, request.user, is_admin=False, content=content, images=images,
                           reply_to=_resolve_dm_reply(request, conv))
        return Response({"success": True, "data": _dm_payload(dm, request)}, status=status.HTTP_201_CREATED)


class SupportInboxView(APIView):
    """Liste des conversations (admins)."""
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=TAG,
        parameters=[OpenApiParameter("q", str, description="Recherche par nom de client")],
        summary="Inbox support — liste des conversations (admin)",
    )
    def get(self, request):
        from django.db.models import Count, Q
        q = (request.query_params.get("q") or "").strip()
        convs = (
            Conversation.objects.select_related("client")
            .annotate(unread=Count("messages", filter=Q(messages__is_admin=False, messages__read_by_admin=False)))
            .filter(last_message_at__isnull=False)
            .order_by("-last_message_at")
        )
        if q:
            convs = convs.filter(
                Q(client__username__icontains=q)
                | Q(client__first_name__icontains=q)
                | Q(client__last_name__icontains=q)
            )
        results = []
        for c in convs:
            last = c.messages.order_by("-created_at").first()
            results.append({
                "id": c.id,
                "client_name": _author_label(c.client),
                "unread_count": c.unread,
                "last_message": (last.content[:60] if last and last.content else ("📷 image" if last else "")),
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
        dm = _send_message(conv, request.user, is_admin=True, content=content, images=images,
                           reply_to=_resolve_dm_reply(request, conv))
        return Response({"success": True, "data": _dm_payload(dm, request)}, status=status.HTTP_201_CREATED)


# ── Modération (admin) ──────────────────────────────────────────────────────
def _moderable_author(pk):
    try:
        msg = Message.objects.select_related("author", "channel").get(pk=pk)
    except Message.DoesNotExist:
        raise ApiError("NOT_FOUND", "Message introuvable.", status_code=404)
    if not msg.author_id or msg.author.is_staff:
        raise ApiError("VALIDATION_ERROR", "Action impossible sur cet utilisateur.")
    return msg


class BanAuthorView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG_MOD, summary="Bannir / débannir l'auteur d'un message")
    def post(self, request, pk):
        msg = _moderable_author(pk)
        ban, created = CommunityBan.objects.get_or_create(
            user=msg.author,
            defaults={"is_active": True, "created_by": request.user, "reason": "Banni depuis l'app"},
        )
        if not created:
            ban.is_active = not ban.is_active
            ban.save(update_fields=["is_active"])
        return Response({"success": True, "banned": ban.is_active, "user": msg.author.username})


class MuteAuthorView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG_MOD, summary="Mute / unmute l'auteur dans ce salon")
    def post(self, request, pk):
        msg = _moderable_author(pk)
        mute = ChannelMute.objects.filter(channel=msg.channel, user=msg.author).first()
        if mute:
            mute.delete()
            muted = False
        else:
            ChannelMute.objects.create(channel=msg.channel, user=msg.author, created_by=request.user)
            muted = True
        return Response({"success": True, "muted": muted, "user": msg.author.username})


class ChannelLockView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG_MOD, summary="Cycle d'accès en écriture d'un salon")
    def post(self, request, slug):
        try:
            ch = Channel.objects.get(slug=slug)
        except Channel.DoesNotExist:
            raise ApiError("NOT_FOUND", "Salon introuvable.", status_code=404)
        order = [Channel.WRITE_OPEN, Channel.WRITE_LOCKED, Channel.WRITE_ADMINS]
        i = order.index(ch.write_access) if ch.write_access in order else 0
        ch.write_access = order[(i + 1) % len(order)]
        ch.save(update_fields=["write_access", "updated_at"])
        return Response({"success": True, "write_access": ch.write_access, "label": ch.get_write_access_display()})


class ChannelAdminListCreateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG_MOD, summary="Tous les salons (gestion) / créer un salon", responses=ChannelAdminSerializer)
    def get(self, request):
        data = ChannelAdminSerializer(Channel.objects.all(), many=True).data
        return Response({"success": True, "results": data})

    @extend_schema(tags=TAG_MOD, request=ChannelAdminSerializer, summary="Créer un salon")
    def post(self, request):
        serializer = ChannelAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ch = serializer.save()
        return Response({"success": True, "data": ChannelAdminSerializer(ch).data}, status=status.HTTP_201_CREATED)


class ChannelAdminUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=TAG_MOD, request=ChannelAdminSerializer, summary="Modifier un salon")
    def patch(self, request, slug):
        try:
            ch = Channel.objects.get(slug=slug)
        except Channel.DoesNotExist:
            raise ApiError("NOT_FOUND", "Salon introuvable.", status_code=404)
        serializer = ChannelAdminSerializer(ch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "data": serializer.data})


class UserSearchView(APIView):
    """Recherche d'utilisateurs pour l'autocomplete @mention."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=TAG,
        parameters=[OpenApiParameter("q", str, description="Texte recherché")],
        summary="Rechercher des utilisateurs à mentionner",
    )
    def get(self, request):
        from django.contrib.auth import get_user_model
        from django.db.models import Q

        q = (request.query_params.get("q") or "").strip()
        User = get_user_model()
        qs = User.objects.filter(is_active=True)
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        results = []
        for u in qs[:10]:
            full = f"{u.first_name} {u.last_name}".strip()
            results.append({"id": u.id, "username": u.username, "name": full or u.username})
        return Response({"success": True, "results": results})
