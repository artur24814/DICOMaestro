import pytest
from django.urls import reverse
from rest_framework import status
from tests.decorators.num_queries import assert_num_queries


BASE_URL = reverse('developer_profile:developer-profile')


@pytest.mark.django_db
@assert_num_queries(1)
def test_get_existing_profile(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    response = api_client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["organization"] == "My Organization"
    assert response.data["purpose"] == "testing"


@pytest.mark.django_db
@assert_num_queries(1)
def test_get_non_existing_profile(api_client, developer_app_user):
    api_client.force_authenticate(user=developer_app_user)
    response = api_client.get(BASE_URL)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Developer profile does not exist."


@pytest.mark.django_db
@assert_num_queries(11)  # + 3 query for conftest
def test_create_profile(api_client, developer_app_user):
    api_client.force_authenticate(user=developer_app_user)
    data = {"purpose": "testing"}
    response = api_client.post(BASE_URL, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["purpose"] == "testing"


@pytest.mark.django_db
@assert_num_queries(4)
def test_update_existing_profile(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    data = {"purpose": "research"}
    response = api_client.post(BASE_URL, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["purpose"] == "research"
