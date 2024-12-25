from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class CookieOrRequestDataJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        if not token:
            raise AuthenticationFailed("Refresh token not found")

        try:
            validated_token = RefreshToken(token)
            user = JWTAuthentication().get_user(validated_token)
        except (AuthenticationFailed, InvalidToken, TokenError):
            raise AuthenticationFailed("Invalid or expired JWT token")

        return (user, validated_token)
