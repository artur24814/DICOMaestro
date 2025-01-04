from django.urls import path
from .views import DeveloperApiKeyAPIView


app_name = 'developer_auth'
urlpatterns = [
    path('api-keys/', DeveloperApiKeyAPIView.as_view(), name='api-key'),
    path('api-keys/delete/<str:pk>/', DeveloperApiKeyAPIView.as_view(), name='api-key-delete'),
]
