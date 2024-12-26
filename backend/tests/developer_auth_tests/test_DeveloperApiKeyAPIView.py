import pytest
from django.urls import reverse
from rest_framework import status

from tests.decorators.num_queries import assert_num_queries
from developer_auth.models import DeveloperAPIKey
from developer_profile.models import DeveloperProfile
from accounts.models import AppUser


BASE_URL = reverse('developer_auth:api-key')


@pytest.mark.django_db
@assert_num_queries(1)
def test_list_api_keys_forbidden_user_is_not_a_developer(api_client, base_app_user, api_key):
    api_client.force_authenticate(user=base_app_user)
    response = api_client.get(BASE_URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == 'You do not have permission to perform this action.'


@pytest.mark.django_db
@assert_num_queries(2)
def test_list_api_keys(api_client, developer_profile, api_key):
    api_client.force_authenticate(user=developer_profile.user)
    response = api_client.get(BASE_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == api_key.name


@pytest.mark.django_db
@assert_num_queries(3)
def test_create_api_key(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    payload = {"name": "new-key"}
    response = api_client.post(BASE_URL, data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert "api_key" in response.data
    assert response.data["name"] == "new-key"


@pytest.mark.django_db
@assert_num_queries(3)
def test_create_api_key_without_name(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    response = api_client.post(BASE_URL, data={})

    assert response.status_code == status.HTTP_201_CREATED
    assert "api_key" in response.data
    assert response.data["name"] == f"{developer_profile.user.first_name}-developer-key"


@pytest.mark.django_db
@assert_num_queries(4)
def test_delete_api_key(api_client, developer_profile, api_key):
    api_client.force_authenticate(user=developer_profile.user)
    response = api_client.delete(BASE_URL + f"delete/{api_key.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert DeveloperAPIKey.objects.filter(id=api_key.id).count() == 0


@pytest.mark.django_db
@assert_num_queries(7)
def test_delete_api_key_unauthorized(api_client, developer_profile, api_key):
    other_user = AppUser.objects.create_user(
        email='OtherTestuser@example.com',
        first_name='John',
        last_name='Doe',
        password='securepassword123'
    )
    DeveloperProfile.objects.create(
        user=other_user,
        purpose="testing",
        organization="My Organization"
    )
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(BASE_URL + f"delete/{api_key.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert DeveloperAPIKey.objects.filter(id=api_key.id).exists()
