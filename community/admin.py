from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Channel,
    ChannelMute,
    CommunityBan,
    Message,
    MessageAttachment,
    MessageReaction,
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
