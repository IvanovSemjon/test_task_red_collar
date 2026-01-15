from rest_framework import serializers
from .models import Point

class PointSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Point
        fields = ("id", "title", "description", "location", "owner", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")