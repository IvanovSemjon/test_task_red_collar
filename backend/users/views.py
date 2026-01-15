from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.GenericViewSet):
    """
    ViewSet для управления пользователями.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Регистрация пользователя + возврат JWT.
        """
        serializer = UserRegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["get", "patch", "put"])
    def me(self, request):
        """
        Просмотр/редактирование текущего пользователя.
        """
        if request.method in ["PATCH", "PUT"]:
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)