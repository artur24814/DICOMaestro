from django.urls import path
from .views import ReadDICOMFileAPIView


app_name = 'dicom_reader'
urlpatterns = [
    path('file/', ReadDICOMFileAPIView.as_view(), name='read-dicom-file')
]
