from django.urls import path

from .views import (
    ChannelListView,
    ChannelMessagesView,
    MessageDeleteView,
    MessageReactView,
)

urlpatterns = [
    path("channels/", ChannelListView.as_view(), name="api-community-channels"),
    path("channels/<slug:slug>/messages/", ChannelMessagesView.as_view(), name="api-community-messages"),
    path("messages/<int:pk>/react/", MessageReactView.as_view(), name="api-community-react"),
    path("messages/<int:pk>/", MessageDeleteView.as_view(), name="api-community-message"),
]
