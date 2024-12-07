from django.urls import path
from .views import DicomAllowedFieldsAPIViews


app_name = 'dicom_format'
urlpatterns = [
    path('allowed-fields/', DicomAllowedFieldsAPIViews.as_view(), name='allowed-fields')
]
