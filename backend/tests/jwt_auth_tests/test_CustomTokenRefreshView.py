import pytest

from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.testing_data.accounts import BASE_USER_DATA
from tests.decorators.num_queries import assert_num_queries

User = get_user_model()
BASE_LOGIN_URL = reverse('jwt_auth:token_obtain_pair')
BASE_TOKEN_REFRESH_URL = reverse('jwt_auth:token_refresh')


@pytest.mark.django_db
@assert_num_queries(1)
def test_custom_token_refresh_view_valid_token(client, base_app_user):
    """
    Test the custom token refresh view with a valid refresh token.
    """

    # Obtain refresh token by logging in
    user_data = BASE_USER_DATA.copy()

    login_data = {
        'email': base_app_user.email,
        'password': user_data['password'],
    }
    response = client.post(BASE_LOGIN_URL, login_data)
    refresh_token = response.data['refresh']

    # Now use this refresh token to get a new access token
    response = client.post(BASE_TOKEN_REFRESH_URL, {'refresh': refresh_token})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data


@pytest.mark.django_db
@assert_num_queries(0)
def test_custom_token_refresh_view_invalid_token(client):
    """
    Test the custom token refresh view with an invalid or expired refresh token.
    """
    refresh_token = 'invalid_or_expired_refresh_token'
    response = client.post(BASE_TOKEN_REFRESH_URL, {'refresh': refresh_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['error'] == 'Invalid or expired refresh token'


@pytest.mark.django_db
@assert_num_queries(0)
def test_custom_token_refresh_view_missing_token(client):
    """
    Test the custom token refresh view when the refresh token is missing from cookies.
    """
    response = client.post('/api/token/refresh/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Refresh token not found in cookies'
