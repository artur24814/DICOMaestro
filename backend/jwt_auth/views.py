from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

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
    def post(self, request, *args, **kwargs):
        if (refresh_token := request.COOKIES.get('refresh_token')):               
            request.data['refresh'] = refresh_token

            try:
                refresh = RefreshToken(refresh_token)
                access_token = refresh.access_token

                return Response({
                    'access': str(access_token), 
                })
            except InvalidToken:
                return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'Refresh token not found in cookies'}, status=status.HTTP_400_BAD_REQUEST)
