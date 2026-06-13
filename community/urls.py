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
]
