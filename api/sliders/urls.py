from django.urls import path

from api.sliders.views import SliderListView

urlpatterns = [
    path("", SliderListView.as_view(), name="api-slider-list"),
]
