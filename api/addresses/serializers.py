from rest_framework import serializers

from dashboard.models.Adress import Adress


class AddressSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField()

    class Meta:
        model = Adress
        fields = [
            "id", "full_name", "street", "city",
            "phone", "more_details", "adress_type",
            "is_default", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_is_default(self, obj):
        # Graceful: support is_default field if migration was applied
        return getattr(obj, "is_default", False)

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
