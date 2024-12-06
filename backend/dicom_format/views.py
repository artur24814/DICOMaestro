from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_allowed_dicom_fields, get_dicom_version


class DicomAllowedFieldsAPIViews(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "allowedFields": get_allowed_dicom_fields(),
            "dicomVersion": get_dicom_version()
        }
        return Response(data, status=status.HTTP_200_OK)
