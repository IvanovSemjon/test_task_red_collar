from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        label="Пароль"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Повторите пароль"
    )
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "display_name", "alliance_name", "avatar", "password", "password2", "token")
        extra_kwargs = {
            'display_name': {'label': 'Позывной'},
            'alliance_name': {'label': 'Название сообщества'},
            'avatar': {'label': 'Аватар'},
            'username': {'label': 'Имя пользователя'},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "display_name", "alliance_name", "avatar")