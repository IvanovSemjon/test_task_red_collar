"""Сериалайзер для пользователя."""
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    """Регистрация пользователя."""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        label="Пароль"
        )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        label="Повторите пароль")

    class Meta:
        """
        Мета класс UserRegisterSerializer"""
        model = CustomUser
        fields = ("id", "username", "display_name", "alliance_name", "avatar", "password", "password2")
        extra_kwargs = {
            'display_name': {'label': 'Позывной'},
            'alliance_name': {'label': 'Название сообщества'},
            'avatar': {'label': 'Аватар'},
            'username': {'label': 'Имя пользователя'},
        }
    
    def validate(self, attrs):
        """
        Валидация паролей
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        """
        Создание пароля"""
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "display_name", "alliance_name", "avatar")