from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from .authentications import CookieOrRequestDataJWTAuthentication

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh_token = response.data['refresh']
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            max_age=30*24*60*60
        )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [CookieOrRequestDataJWTAuthentication]

    def post(self, request, *args, **kwargs):
        access_token = request.auth
        return Response({
            'access': str(access_token),
        })
