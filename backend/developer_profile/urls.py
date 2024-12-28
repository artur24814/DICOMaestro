from django.urls import path
from .views import RetreveCreateDeveloperProfileAPIView, DeveloperActivitySummaryView


app_name = 'developer_profile'
urlpatterns = [
    path('', RetreveCreateDeveloperProfileAPIView.as_view(), name='developer-profile'),
    path('activity-summary/', DeveloperActivitySummaryView.as_view(), name='activity-summary')
]
