from django.urls import path
from .views import DicomAllowedFieldsAPIViews, DicomRequiredFileldTypeAPIView


app_name = 'dicom_format'
urlpatterns = [
    path('allowed-fields/', DicomAllowedFieldsAPIViews.as_view(), name='allowed-fields'),
    path('required-field-type/', DicomRequiredFileldTypeAPIView.as_view(), name='required-field-type')
]
