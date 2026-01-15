from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D

from .models import Point
from .serializers import PointSerializer
from .permissions import IsOwnerOrReadOnly
from .models import PointMessage
from .serializers import PointMessageSerializer


class PointViewSet(viewsets.ModelViewSet):
    """
    Управление точками на карте.
    """
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['post', 'get']

    def get_queryset(self):
        """
        Все точки доступны для чтения авторизованным пользователям.
        """
        return Point.objects.none()   # pylint: disable=no-member

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Поиск точек в радиусе.
        """
        try:
            lat = float(request.query_params["latitude"])
            lon = float(request.query_params["longitude"])
            radius_km = float(request.query_params["radius"])
        except (KeyError, TypeError, ValueError):
            return Response(
                {"error": "latitude, longitude и radius обязательны"},
                status=400,
            )

        user_location = GeoPoint(lon, lat, srid=4326)

        points = Point.objects.filter(    # pylint: disable=no-member
            location__distance_lte=(user_location, D(km=radius_km))
        )

        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)
    

class PointMessageViewSet(viewsets.ModelViewSet):
    """
    Сообщения, привязанные к точкам.
    """
    serializer_class = PointMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'get']

    def get_queryset(self):
        """
        Все сообщения доступны авторизованным пользователям.
        """
        return PointMessage.objects.none()  # pylint: disable=no-member

    def perform_create(self, serializer):
        """
        Создание сообщения от имени текущего пользователя.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def search_by_radius(self, request):
        """
        Поиск сообщений по радиусу.
        """
        try:
            lat = float(request.query_params["latitude"])
            lon = float(request.query_params["longitude"])
            radius_km = float(request.query_params["radius"])
        except (KeyError, TypeError, ValueError):
            return Response(
                {"error": "latitude, longitude и radius обязательны"},
                status=400,
            )

        user_location = GeoPoint(lon, lat, srid=4326)

        messages = PointMessage.objects.filter(  # pylint: disable=no-member
            point__location__distance_lte=(user_location, D(km=radius_km))
        ).select_related("point", "user")

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)