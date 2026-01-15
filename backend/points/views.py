"""ViewSet для управления точками и поиска по радиусу."""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D
from .models import Point
from .serializers import PointSerializer

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all().order_by("-created_at")
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Поиск точек в радиусе:
        GET /api/points/search/?latitude=...&longitude=...&radius=...
        """
        try:
            lat = float(request.query_params.get("latitude"))
            lon = float(request.query_params.get("longitude"))
            radius_km = float(request.query_params.get("radius"))
        except (TypeError, ValueError):
            return Response({"error": "Invalid or missing parameters"}, status=400)

        user_location = GeoPoint(lon, lat, srid=4326)
        points = Point.objects.filter(location__distance_lte=(user_location, D(km=radius_km)))

        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)