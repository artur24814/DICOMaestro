import pytest
import jwt

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings

from tests.testing_data.accounts import BASE_USER_DATA

User = get_user_model()
BASE_URL = reverse('jwt_auth:token_obtain_pair')


@pytest.mark.django_db
def test_custom_token_obtain_pair_view(client, base_app_user):
    """
    Test the custom token obtain view (JWT obtain access and refresh tokens).
    """
    user_data = BASE_USER_DATA.copy()

    login_data = {
        'email': base_app_user.email,
        'password': user_data['password'],
    }
    response = client.post(BASE_URL, login_data)

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

    # Assert that the refresh token is set as a cookie
    assert 'refresh_token' in response.cookies

    # Decode the access token to verify the payload
    access_token = response.data['access']
    decoded_token = jwt.decode(
        access_token,
        api_settings.SIGNING_KEY,
        algorithms=[api_settings.ALGORITHM]
    )

    # Assert that the custom claims are present and correct
    assert decoded_token['first_name'] == 'John'
    assert decoded_token['last_name'] == 'Doe'
