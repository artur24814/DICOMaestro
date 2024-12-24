import pytest

from rest_framework.test import APIClient
from django.test import Client

from accounts.models import AppUser
from developer_accounts.models import DeveloperAPIKey

from .testing_data.accounts import BASE_USER_DATA


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def base_app_user():
    user = AppUser.objects.create_user(
        **BASE_USER_DATA
    )
    return user


@pytest.fixture
def api_key(base_app_user):
    key_name = "test-key"
    api_key, _ = DeveloperAPIKey.objects.create_key(name=key_name, user=base_app_user)
    return api_key
