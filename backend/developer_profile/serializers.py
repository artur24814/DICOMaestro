from rest_framework import serializers
from .models import DeveloperProfile


class DeveloperProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ("purpose", "organization")
