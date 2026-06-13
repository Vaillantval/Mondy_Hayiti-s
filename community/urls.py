from django.urls import path

from . import support_views, views

app_name = "community"

urlpatterns = [
    path("", views.community_home, name="home"),
    path("c/<slug:slug>/", views.community_home, name="channel"),

    # Endpoints JSON (polling + actions)
    path("c/<slug:slug>/feed/", views.messages_feed, name="feed"),
    path("c/<slug:slug>/post/", views.post_message, name="post"),
    path("m/<int:message_id>/react/", views.react_message, name="react"),
    path("m/<int:message_id>/delete/", views.delete_message, name="delete"),
    path("m/<int:message_id>/pin/", views.pin_message, name="pin"),
    path("products/search/", views.product_search, name="product_search"),

    # Modération in-UI (staff)
    path("m/<int:message_id>/ban-author/", views.ban_author, name="ban_author"),
    path("m/<int:message_id>/mute-author/", views.mute_author, name="mute_author"),
    path("c/<slug:slug>/lock/", views.lock_channel, name="lock_channel"),
    path("manage/channels/", views.manage_channels, name="manage_channels"),
    path("manage/channels/save/", views.channel_save, name="channel_save"),

    # Abonnement salon
    path("c/<slug:slug>/subscribe/", views.channel_subscribe, name="subscribe"),

    # Notifications
    path("notifications/feed/", views.notifications_feed, name="notifications_feed"),
    path("notifications/read/", views.notifications_read, name="notifications_read"),

    # Web Push
    path("push/subscribe/", views.push_subscribe, name="push_subscribe"),
    path("push/unsubscribe/", views.push_unsubscribe, name="push_unsubscribe"),

    # Support privé — côté client
    path("support/", support_views.support_home, name="support"),
    path("support/feed/", support_views.support_feed, name="support_feed"),
    path("support/post/", support_views.support_post, name="support_post"),

    # Support privé — côté admin (inbox partagée)
    path("inbox/", support_views.inbox, name="inbox"),
    path("inbox/<int:conv_id>/", support_views.inbox_conversation, name="inbox_conversation"),
    path("inbox/<int:conv_id>/feed/", support_views.inbox_feed, name="inbox_feed"),
    path("inbox/<int:conv_id>/post/", support_views.inbox_post, name="inbox_post"),
]
