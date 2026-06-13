from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.sliders.serializers import SliderSerializer
from shop.models.Slider import Slider


class SliderListView(generics.ListAPIView):
    """Hero slides de la page d'accueil (carrousel)."""

    serializer_class = SliderSerializer
    permission_classes = [AllowAny]
    queryset = Slider.objects.all().order_by("created_at")

    @extend_schema(tags=["Accueil"], summary="Hero slides (carrousel d'accueil)")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
