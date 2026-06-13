from rest_framework import serializers

from shop.models.Slider import Slider


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["id", "title", "description", "button_text", "button_link", "image"]
