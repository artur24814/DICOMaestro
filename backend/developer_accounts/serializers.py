from rest_framework import serializers
from .models import DeveloperAPIKey


class DeveloperApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperAPIKey
        fields = ("id", "name", "created", "revoked", "expiry_date")


class CreateDeveloperApiKeySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500, allow_blank=True, required=False)

    def create(self, validated_data):
        if not (key_name := validated_data.get("name", None)) or key_name == "":
            key_name = f"{self.context['request'].user.first_name}-developer-key"
        _, key = DeveloperAPIKey.objects.create_key(name=key_name, user=self.context['request'].user)
        return {"api_key": key, "name": key_name}
