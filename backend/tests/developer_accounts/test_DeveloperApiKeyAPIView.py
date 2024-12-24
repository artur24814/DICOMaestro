import pytest
from django.urls import reverse

from tests.decorators.num_queries import assert_num_queries
from developer_accounts.models import DeveloperAPIKey
from accounts.models import AppUser


BASE_URL = reverse('developer_accounts:api-key')


@pytest.mark.django_db
@assert_num_queries(1)
def test_list_api_keys(api_client, base_app_user, api_key):
    api_client.force_authenticate(user=base_app_user)
    response = api_client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == api_key.name


@pytest.mark.django_db
@assert_num_queries(2)
def test_create_api_key(api_client, base_app_user):
    api_client.force_authenticate(user=base_app_user)
    payload = {"name": "new-key"}
    response = api_client.post(BASE_URL, data=payload)

    assert response.status_code == 201
    assert "api_key" in response.data
    assert response.data["name"] == "new-key"


@pytest.mark.django_db
@assert_num_queries(2)
def test_create_api_key_without_name(api_client, base_app_user):
    api_client.force_authenticate(user=base_app_user)
    response = api_client.post(BASE_URL, data={})

    assert response.status_code == 201
    assert "api_key" in response.data
    assert response.data["name"] == f"{base_app_user.first_name}-developer-key"


@pytest.mark.django_db
@assert_num_queries(3)
def test_delete_api_key(api_client, base_app_user, api_key):
    api_client.force_authenticate(user=base_app_user)
    response = api_client.delete(BASE_URL + f"delete/{api_key.id}/")

    assert response.status_code == 204
    assert DeveloperAPIKey.objects.filter(id=api_key.id).count() == 0


@pytest.mark.django_db
@assert_num_queries(3)
def test_delete_api_key_unauthorized(api_client, base_app_user, api_key):
    other_user = AppUser.objects.create_user(
        email='OtherTestuser@example.com',
        first_name='John',
        last_name='Doe',
        password='securepassword123'
    )
    api_client.force_authenticate(user=other_user)
    response = api_client.delete(BASE_URL + f"delete/{api_key.id}/")

    assert response.status_code == 404
    assert DeveloperAPIKey.objects.filter(id=api_key.id).exists()
