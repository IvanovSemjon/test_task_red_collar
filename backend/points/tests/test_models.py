import pytest  # pylint: disable=import-error

from django.contrib.gis.geos import Point
from points.models import Point as GeoPoint, PointMessage

def test_point_creation(user):
    point = GeoPoint.objects.create(   # pylint: disable=no-member
        owner=user,
        title="Точка 1",
        description="Описание",
        location=Point(37.618423, 55.751244)
    )
    assert point.title == "Точка 1"
    assert point.owner == user
    assert point.location.x == 37.618423
    assert point.location.y == 55.751244

def test_point_message_creation(user, point):
    msg = PointMessage.objects.create(   # pylint: disable=no-member
        point=point,
        user=user,
        text="Тестовое сообщение"
    )
    assert msg.point == point
    assert msg.user == user
    assert msg.text == "Тестовое сообщение"