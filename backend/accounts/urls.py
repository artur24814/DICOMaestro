from .views import UserRegisterAPIView
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name="register")
]
