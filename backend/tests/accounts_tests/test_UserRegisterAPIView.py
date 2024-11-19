import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from tests.testing_data.accounts import BASE_USER_DATA

User = get_user_model()
BASE_URL = reverse('accounts:register')


@pytest.mark.django_db
def test_user_registration_success(client):
    """
    Test the successful user registration process.
    """
    user_data = BASE_USER_DATA.copy()
    response = client.post(BASE_URL, user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully!'

    # Ensure the user has been created in the database
    user = User.objects.get(email=user_data['email'])
    assert user.first_name == user_data['first_name']
    assert user.last_name == user_data['last_name']
    assert user.check_password(user_data['password'])


@pytest.mark.django_db
def test_user_registration_duplicate_email(client, base_app_user):
    """
    Test registration with a duplicate email, expecting a validation error.
    """
    user_data = BASE_USER_DATA.copy()
    response = client.post(BASE_URL, user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == ['user with this email already exists.']


@pytest.mark.django_db
def test_user_registration_missing_fields(client):
    """
    Test registration when required fields are missing.
    """
    # Prepare user data with missing 'email'
    user_data = BASE_USER_DATA.copy()
    del user_data['email']

    response = client.post(BASE_URL, user_data)

    # Assert the response status code and validation error message
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data


@pytest.mark.django_db
def test_user_registration_weak_password(client):
    """
    Test registration with a weak password (too short).
    """
    # Prepare user data with a weak password
    user_data = BASE_USER_DATA.copy()
    user_data['password'] = 'short'

    response = client.post(BASE_URL, user_data)

    # Assert the response status code and validation error message
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data
    assert response.data['password'] == ['Ensure this field has at least 8 characters.']
