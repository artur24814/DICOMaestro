from .views import UserRegisterAPIView
from django.urls import path


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name="register")
]
