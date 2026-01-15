from rest_framework import serializers
from .models import Point, PointMessage

class PointSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели точки.
    """
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Point
        fields = ("id", "title", "description", "location", "owner", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")


class PointMessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели сообщений к точке.
    """
    user = serializers.StringRelatedField(read_only=True)
    point = serializers.PrimaryKeyRelatedField(queryset=None)

    class Meta:
        """
         Мета информация для сериализатора сообщений к точке."""
        model = PointMessage
        fields = ("id", "point", "user", "text", "file", "image", "created_at")
        read_only_fields = ("id", "user", "created_at")

    def __init__(self, *args, **kwargs):
        """
        Мета информация для инициализации сериализатора сообщений к точке.
        """
        super().__init__(*args, **kwargs)
        self.fields["point"].queryset = self.context["request"].user.points.all()