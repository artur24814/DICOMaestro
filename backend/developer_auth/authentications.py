from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import DeveloperAPIKey


class APIKeyAuthentication(BaseAuthentication):

    def authenticate(self, request) -> tuple:
        api_key = request.headers.get("Authorization")
        if not api_key:
            return None

        api_key = api_key.replace("ApiKey ", "") if api_key.startswith("ApiKey ") else api_key

        try:
            key = DeveloperAPIKey.objects.get_from_key(api_key)
        except DeveloperAPIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid or missing API key.")

        if key.revoked:
            raise AuthenticationFailed("This API key has been revoked.")

        return (key.user, key)
