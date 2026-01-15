import pytest   # pylint: disable=import-error

from rest_framework import status
from django.contrib.gis.geos import Point as GeoPoint
from points.models import Point, PointMessage
from users.models import CustomUser
import tempfile

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(username="testuser", password="pass1234")

@pytest.fixture
def point(user):
    """
    Создаём точку для тестов
    """
    return Point.objects.create(  # pylint: disable=no-member
        owner=user,
        title="Тестовая точка",
        description="Описание",
        location=GeoPoint(37.618423, 55.751244, srid=4326)
    )

@pytest.mark.django_db
def test_create_point(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "title": "Новая точка",
        "description": "Описание новой точки",
        "location": {"type": "Point", "coordinates": [37.618423, 55.751244]}
    }
    response = api_client.post("/api/points/", data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Point.objects.filter(title="Новая точка").exists()  # pylint: disable=no-member

@pytest.mark.django_db
def test_get_points(api_client, user, point):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/points/")
    assert response.status_code == 200
    assert any(p["id"] == point.id for p in response.data)

@pytest.mark.django_db
def test_search_points_radius(api_client, user, point):
    api_client.force_authenticate(user=user)
    params = {"latitude": 55.751244, "longitude": 37.618423, "radius": 5}
    response = api_client.get("/api/points/search/", params)
    assert response.status_code == 200
    assert any(p["id"] == point.id for p in response.data)

@pytest.mark.django_db
def test_create_point_message(api_client, user, point):
    api_client.force_authenticate(user=user)
    temp_file = tempfile.NamedTemporaryFile(suffix=".txt")
    temp_file.write(b"test content")
    temp_file.seek(0)

    data = {
        "point": point.id,
        "text": "Тестовое сообщение",
        "file": temp_file
    }
    response = api_client.post("/api/points/messages/", data, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert PointMessage.objects.filter(text="Тестовое сообщение").exists()  # pylint: disable=no-member

@pytest.mark.django_db
def test_search_messages_radius(api_client, user, point):
    api_client.force_authenticate(user=user)
    msg = PointMessage.objects.create(  # pylint: disable=no-member
        point=point,
        user=user,
        text="Сообщение для поиска"
    )
    params = {"latitude": 55.751244, "longitude": 37.618423, "radius": 5}
    response = api_client.get("/api/points/messages/search_by_radius/", params)
    assert response.status_code == 200
    assert any(m["id"] == msg.id for m in response.data)

@pytest.mark.django_db
def test_point_permission(api_client, point):
    other_user = CustomUser.objects.create_user(username="otheruser", password="pass1234")
    api_client.force_authenticate(user=other_user)

    data = {"title": "Изменённое название"}
    response = api_client.patch(f"/api/points/{point.id}/", data, format="json")
    assert response.status_code in [403, 405]