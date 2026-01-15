import pytest  # pylint: disable=import-error
from django.contrib.gis.geos import Point
from users.models import CustomUser
from points.models import Point as GeoPoint

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(username="testuser", password="pass1234")

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def point(user):
    return GeoPoint.objects.create(   # pylint: disable=no-member
        owner=user,
        title="Тестовая точка",
        description="Описание точки",
        location=Point(37.618423, 55.751244)
    )