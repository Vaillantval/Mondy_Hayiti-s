from django.urls import path

from .views import (
    BanAuthorView,
    ChannelAdminListCreateView,
    ChannelAdminUpdateView,
    ChannelListView,
    ChannelLockView,
    ChannelMessagesView,
    ChannelSubscribeView,
    MessageDeleteView,
    MessageReactView,
    MuteAuthorView,
    NotificationListView,
    SupportInboxMessagesView,
    SupportInboxView,
    SupportMessagesView,
    UserSearchView,
)

urlpatterns = [
    path("channels/", ChannelListView.as_view(), name="api-community-channels"),
    path("channels/<slug:slug>/messages/", ChannelMessagesView.as_view(), name="api-community-messages"),
    path("channels/<slug:slug>/subscribe/", ChannelSubscribeView.as_view(), name="api-community-subscribe"),
    path("messages/<int:pk>/react/", MessageReactView.as_view(), name="api-community-react"),
    path("messages/<int:pk>/", MessageDeleteView.as_view(), name="api-community-message"),
    path("notifications/", NotificationListView.as_view(), name="api-community-notifications"),

    # Support privé
    path("support/messages/", SupportMessagesView.as_view(), name="api-community-support"),
    path("support/inbox/", SupportInboxView.as_view(), name="api-community-inbox"),
    path("support/inbox/<int:conv_id>/messages/", SupportInboxMessagesView.as_view(), name="api-community-inbox-messages"),

    # Mentions
    path("users/search/", UserSearchView.as_view(), name="api-community-users-search"),

    # Modération (admin)
    path("messages/<int:pk>/ban-author/", BanAuthorView.as_view(), name="api-community-ban"),
    path("messages/<int:pk>/mute-author/", MuteAuthorView.as_view(), name="api-community-mute"),
    path("channels/<slug:slug>/lock/", ChannelLockView.as_view(), name="api-community-lock"),
    path("manage/channels/", ChannelAdminListCreateView.as_view(), name="api-community-manage-channels"),
    path("manage/channels/<slug:slug>/", ChannelAdminUpdateView.as_view(), name="api-community-manage-channel"),
]
