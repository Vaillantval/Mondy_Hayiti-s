from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Channel,
    ChannelMute,
    ChannelSubscription,
    CommunityBan,
    Conversation,
    DirectMessage,
    DirectMessageAttachment,
    Message,
    MessageAttachment,
    MessageReaction,
    Notification,
    WebPushToken,
)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("emoji", "name", "slug", "read_access", "write_access", "is_active", "order")
    list_display_links = ("name",)
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "read_access", "write_access")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "channel", "author", "short_content", "product", "is_pinned", "is_deleted", "created_at")
    list_filter = ("channel", "is_pinned", "is_deleted", "created_at")
    search_fields = ("content", "author__username")
    raw_id_fields = ("author", "product", "reply_to", "channel", "deleted_by")
    readonly_fields = ("created_at", "updated_at")
    inlines = [MessageAttachmentInline]
    actions = ("action_pin", "action_unpin", "action_soft_delete", "action_restore")

    @admin.display(description="Contenu")
    def short_content(self, obj):
        return (obj.content[:60] + "…") if len(obj.content) > 60 else obj.content

    @admin.action(description="📌 Épingler les messages sélectionnés")
    def action_pin(self, request, queryset):
        queryset.update(is_pinned=True)

    @admin.action(description="Retirer l'épingle")
    def action_unpin(self, request, queryset):
        queryset.update(is_pinned=False)

    @admin.action(description="🗑️ Masquer (suppression douce)")
    def action_soft_delete(self, request, queryset):
        queryset.update(is_deleted=True, deleted_by=request.user)

    @admin.action(description="♻️ Restaurer les messages")
    def action_restore(self, request, queryset):
        queryset.update(is_deleted=False)


@admin.register(CommunityBan)
class CommunityBanAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "can_read", "reason", "created_at")
    list_filter = ("is_active", "can_read")
    search_fields = ("user__username", "reason")
    raw_id_fields = ("user", "created_by")

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ChannelMute)
class ChannelMuteAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "reason", "created_at")
    list_filter = ("channel",)
    search_fields = ("user__username", "reason")
    raw_id_fields = ("user", "channel", "created_by")

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    list_display = ("emoji", "user", "message", "created_at")
    search_fields = ("user__username",)


class DirectMessageInline(admin.TabularInline):
    model = DirectMessage
    extra = 0
    fields = ("is_admin", "sender", "content", "read_by_admin", "read_by_client", "created_at")
    readonly_fields = ("created_at",)
    raw_id_fields = ("sender",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("client", "last_message_at", "is_archived", "created_at")
    list_filter = ("is_archived",)
    search_fields = ("client__username",)
    raw_id_fields = ("client",)
    inlines = [DirectMessageInline]


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "is_admin", "sender", "short", "created_at")
    list_filter = ("is_admin", "created_at")
    search_fields = ("content", "sender__username")
    raw_id_fields = ("conversation", "sender")

    @admin.display(description="Contenu")
    def short(self, obj):
        return (obj.content[:50] + "…") if len(obj.content) > 50 else obj.content


@admin.register(ChannelSubscription)
class ChannelSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "muted", "created_at")
    list_filter = ("channel", "muted")
    search_fields = ("user__username",)
    raw_id_fields = ("user", "channel")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "type", "actor", "channel", "count", "is_read", "updated_at")
    list_filter = ("type", "is_read")
    search_fields = ("recipient__username",)
    raw_id_fields = ("recipient", "actor", "channel", "message", "conversation")


@admin.register(WebPushToken)
class WebPushTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "user_agent", "created_at", "last_seen")
    search_fields = ("user__username",)
    raw_id_fields = ("user",)


admin.site.register(DirectMessageAttachment)
