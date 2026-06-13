from django.urls import path

from . import views

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

    # Abonnement salon
    path("c/<slug:slug>/subscribe/", views.channel_subscribe, name="subscribe"),

    # Notifications
    path("notifications/feed/", views.notifications_feed, name="notifications_feed"),
    path("notifications/read/", views.notifications_read, name="notifications_read"),

    # Web Push
    path("push/subscribe/", views.push_subscribe, name="push_subscribe"),
    path("push/unsubscribe/", views.push_unsubscribe, name="push_unsubscribe"),
]
