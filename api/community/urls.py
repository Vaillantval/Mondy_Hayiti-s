from django.urls import path

from .views import (
    ChannelListView,
    ChannelMessagesView,
    ChannelSubscribeView,
    MessageDeleteView,
    MessageReactView,
    NotificationListView,
    SupportInboxMessagesView,
    SupportInboxView,
    SupportMessagesView,
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
]
