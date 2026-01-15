import pytest
from points.serializers import PointSerializer, PointMessageSerializer
from django.contrib.gis.geos import Point
from points.models import Point as GeoPoint, PointMessage

def test_point_serializer(user):
    point = GeoPoint.objects.create(   # pylint: disable=no-member
        owner=user,
        title="Точка 2",
        location=Point(37.618423, 55.751244)
    )
    serializer = PointSerializer(point)
    data = serializer.data
    assert data["title"] == "Точка 2"
    assert "owner_display_name" in data
    assert "owner_avatar" in data

def test_point_message_serializer(user, point):
    msg = PointMessage.objects.create(point=point, user=user, text="Текст")  # pylint: disable=no-member
    serializer = PointMessageSerializer(msg)
    data = serializer.data
    assert data["text"] == "Текст"
    assert data["user_display_name"] == user.display_name or user.username