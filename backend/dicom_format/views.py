import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_allowed_dicom_fields, get_dicom_version
from .serializers import DicomAllowedFieldsFilterQueryParamsSerializer


class DicomAllowedFieldsAPIViews(APIView):
    def get(self, request, *args, **kwargs):
        serializer = DicomAllowedFieldsFilterQueryParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        regex_patterns = serializer.get_patterns()
        allowed_dicom_fields = get_allowed_dicom_fields()

        for pattern in regex_patterns:
            regex = re.compile(pattern)
            allowed_dicom_fields = [field for field in allowed_dicom_fields if regex.match(field)]

        data = {
            "allowedFields": allowed_dicom_fields,
            "dicomVersion": get_dicom_version()
        }
        return Response(data, status=status.HTTP_200_OK)
