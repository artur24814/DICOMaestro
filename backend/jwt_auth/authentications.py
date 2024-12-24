from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('refresh_token')
        if not token:
            return None

        try:
            validated_token = RefreshToken(token)
            user = JWTAuthentication().get_user(validated_token)
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid or expired JWT token")

        return (user, validated_token)
