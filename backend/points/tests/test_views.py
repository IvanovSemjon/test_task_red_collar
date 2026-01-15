import pytest
from rest_framework import status
from django.contrib.gis.geos import Point

@pytest.mark.django_db
def test_create_point(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "title": "Тестовая точка API",
        "description": "Описание API",
        "location": {"type": "Point", "coordinates": [37.618423, 55.751244]}
    }
    response = api_client.post("/api/points/", data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Тестовая точка API"

@pytest.mark.django_db
def test_search_point(api_client, user, point):
    api_client.force_authenticate(user=user)
    response = api_client.get(
        "/api/points/search/?latitude=55.751244&longitude=37.618423&radius=5"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]["title"] == point.title

@pytest.mark.django_db
def test_create_point_message(api_client, user, point):
    api_client.force_authenticate(user=user)
    data = {
        "point": point.id,
        "text": "Сообщение через API"
    }
    response = api_client.post("/api/points/messages/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "Сообщение через API"

@pytest.mark.django_db
def test_search_messages_by_radius(api_client, user, point):
    api_client.force_authenticate(user=user)
    # Создаём сообщение
    api_client.post("/api/points/messages/", {"point": point.id, "text": "Hello"})
    response = api_client.get(
        f"/api/points/messages/search_by_radius/?latitude=55.751244&longitude=37.618423&radius=5"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1