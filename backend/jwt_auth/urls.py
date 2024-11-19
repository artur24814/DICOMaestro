from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView


app_name = 'jwt_auth'
urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
