"""Интеграционные тесты API."""
import pytest  # pylint: disable=import-error
from rest_framework import status
from django.contrib.gis.geos import Point

@pytest.mark.django_db
class TestPointsAPI:
    """Тесты для точек."""
    
    def test_create_point(self, api_client, user):
        """Тест создания точки."""
        api_client.force_authenticate(user=user)
        data = {
            "title": "Тестовая точка",
            "description": "Описание",
            "location": {"type": "Point", "coordinates": [37.618423, 55.751244]}
        }
        response = api_client.post("/api/points/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Тестовая точка"

    def test_list_points(self, api_client, user, point):
        """Тест получения списка точек."""
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/points/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_search_points(self, api_client, user, point):
        """Тест поиска точек в радиусе."""
        api_client.force_authenticate(user=user)
        response = api_client.get(
            "/api/points/search/?latitude=55.751244&longitude=37.618423&radius=5"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

@pytest.mark.django_db
class TestMessagesAPI:
    """Тесты для сообщений."""
    
    def test_create_message(self, api_client, user, point):
        """Тест создания сообщения."""
        api_client.force_authenticate(user=user)
        data = {
            "point": point.id,
            "text": "Тестовое сообщение"
        }
        response = api_client.post("/api/messages/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "Тестовое сообщение"

    def test_search_messages_by_radius(self, api_client, user, point):
        """Тест поиска сообщений в радиусе."""
        api_client.force_authenticate(user=user)
        api_client.post("/api/messages/", {"point": point.id, "text": "Test"})
        response = api_client.get(
            "/api/messages/search_by_radius/?latitude=55.751244&longitude=37.618423&radius=5"
        )
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestThrottling:
    """Тесты throttling."""
    
    def test_throttling_works(self, api_client, user):
        """Проверка работы rate limiting."""
        api_client.force_authenticate(user=user)
        for _ in range(5):
            response = api_client.get("/api/points/")
            assert response.status_code == status.HTTP_200_OK
