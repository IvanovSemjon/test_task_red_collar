from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает чтение всем авторизованным,
    а изменение — только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Получение разрешений.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsMessageOwnerOrReadOnly(BasePermission):
    """
    Чтение — всем авторизованным,
    изменение и удаление — только автору сообщения.
    """

    def has_object_permission(self, request, view, obj):
        """
        Получение разрешений.
        """
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user