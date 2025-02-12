from django.urls import path
from .views import DicomFileDataSetContentUploadAPIView


app_name = 'dicom_writer'
urlpatterns = [
    path('upload_content/', DicomFileDataSetContentUploadAPIView.as_view(), name='upload-content-for-dicom-image')
]
