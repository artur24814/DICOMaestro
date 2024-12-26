import pytest

from rest_framework.test import APIClient
from django.test import Client

from accounts.models import AppUser
from developer_auth.models import DeveloperAPIKey
from developer_profile.models import DeveloperProfile

from .testing_data.accounts import BASE_USER_DATA
from .testing_data.developer_profile import DEVELOPER_USER_DATA, DEVELOPER_PROFILE_DATA


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
def developer_app_user():
    user = AppUser.objects.create_user(
        **DEVELOPER_USER_DATA
    )
    return user


@pytest.fixture
def developer_profile(developer_app_user):
    profile = DeveloperProfile.objects.prefetch_related("user").create(
        user=developer_app_user,
        **DEVELOPER_PROFILE_DATA
    )
    return profile


@pytest.fixture
def api_key(developer_app_user):
    key_name = "test-key"
    api_key, _ = DeveloperAPIKey.objects.create_key(name=key_name, user=developer_app_user)
    return api_key
