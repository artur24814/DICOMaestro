from django.urls import path
from .views import DicomFileDataSetUploadAPIView


app_name = 'dicom_writer'
urlpatterns = [
    path('upload_content/', DicomFileDataSetUploadAPIView.as_view(), name='upload-content-for-dicom-image')
]
