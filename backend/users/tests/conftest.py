import pytest   # pylint: disable=no-member

from users.models import CustomUser
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(username="testuser", password="pass1234")