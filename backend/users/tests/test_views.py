import pytest  # pylint: disable=no-member

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
import tempfile


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(username="testuser", password="pass1234")

@pytest.mark.django_db
def test_user_registration(api_client):
    """
    POST /api/users/register/
    Проверка создания пользователя и возврата JWT токена
    """
    data = {
        "username": "newuser",
        "password": "TestPass123!",
        "password2": "TestPass123!",
        "display_name": "Новый пользователь"
    }
    response = api_client.post("/api/users/register/", data)
    assert response.status_code == status.HTTP_201_CREATED
    user = CustomUser.objects.get(username="newuser")
    assert user is not None
    assert "token" in response.data
    assert "access" in response.data["token"]
    assert "refresh" in response.data["token"]

@pytest.mark.django_db
def test_registration_password_mismatch(api_client):
    """
    Проверка ошибки при несовпадении паролей
    """
    data = {
        "username": "user2",
        "password": "Pass1!",
        "password2": "Pass2!",
    }
    response = api_client.post("/api/users/register/", data)
    assert response.status_code == 400
    assert "password" in response.data

@pytest.mark.django_db
def test_jwt_login(api_client, user):
    """
    POST /api/auth/login/ возвращает access и refresh токены
    """
    data = {"username": user.username, "password": "pass1234"}
    response = api_client.post("/api/auth/login/", data)
    assert response.status_code == 200
    assert "access" in response.data and "refresh" in response.data

@pytest.mark.django_db
def test_jwt_login_invalid(api_client):
    """
    Проверка ошибки логина с неверным паролем
    """
    data = {"username": "nonuser", "password": "wrong"}
    response = api_client.post("/api/auth/login/", data)
    assert response.status_code == 401

@pytest.mark.django_db
def test_jwt_refresh(api_client, user):
    """
    POST /api/auth/refresh/ обновляет access токен
    """
    refresh = RefreshToken.for_user(user)
    data = {"refresh": str(refresh)}
    response = api_client.post("/api/auth/refresh/", data)
    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_user_me_get(api_client, user):
    """
    GET /api/users/me/ возвращает данные текущего пользователя
    """
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/users/me/")
    assert response.status_code == 200
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_user_me_patch_avatar(api_client, user):
    """
    PATCH /api/users/me/ позволяет обновить аватар пользователя
    """
    api_client.force_authenticate(user=user)

    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    temp_file.write(b"fake image content")
    temp_file.seek(0)

    response = api_client.patch(
        "/api/users/me/",
        {"avatar": temp_file},
        format="multipart"
    )
    assert response.status_code == 200
    assert "avatar" in response.data


@pytest.mark.django_db
def test_user_me_unauthenticated(api_client):
    """
    GET /api/users/me/ без токена возвращает 401
    """
    response = api_client.get("/api/users/me/")
    assert response.status_code == 401
