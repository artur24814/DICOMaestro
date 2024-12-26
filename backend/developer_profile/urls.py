from django.urls import path
from .views import RetreveCreateDeveloperProfileAPIView


app_name = 'developer_profile'
urlpatterns = [
    path('', RetreveCreateDeveloperProfileAPIView.as_view(), name='developer-profile'),
]
