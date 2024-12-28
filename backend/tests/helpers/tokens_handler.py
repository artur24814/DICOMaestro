from django.urls import reverse

BASE_LOGIN_URL = reverse('jwt_auth:token_obtain_pair')
BASE_TOKEN_REFRESH_URL = reverse('jwt_auth:token_refresh')


def get_access_key(api_client, user_data: dict) -> str:
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }
    response = api_client.post(BASE_LOGIN_URL, login_data)
    return response.data['access']
