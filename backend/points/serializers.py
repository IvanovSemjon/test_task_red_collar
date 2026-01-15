from rest_framework import serializers
from .models import Point, PointMessage

class PointSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели точки.
    Показывает display_name и аватар владельца.
    """
    owner_display_name = serializers.CharField(source="owner.display_name", read_only=True)
    owner_avatar = serializers.ImageField(source="owner.avatar", read_only=True)

    class Meta:
        model = Point
        fields = (
            "id", "title", "description", "location", 
            "owner", "owner_display_name", "owner_avatar",
            "created_at", "updated_at"
        )
        read_only_fields = ("id", "owner", "owner_display_name", "owner_avatar", "created_at", "updated_at")


class PointMessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор сообщений к точкам.
    Показывает display_name и аватар пользователя.
    """
    user_display_name = serializers.CharField(source="user.display_name", read_only=True)
    user_avatar = serializers.ImageField(source="user.avatar", read_only=True)
    point = serializers.PrimaryKeyRelatedField(queryset=Point.objects.all())

    class Meta:
        model = PointMessage
        fields = (
            "id", "point", "user", "user_display_name", "user_avatar",
            "text", "file", "image", "created_at"
        )
        read_only_fields = ("id", "user", "user_display_name", "user_avatar", "created_at")

    def validate_point(self, point):
        """
        Проверка существования точки.
        """
        if not point:
            raise serializers.ValidationError("Точка не существует")
        return point