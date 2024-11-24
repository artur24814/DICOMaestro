import pydicom
from pydicom.errors import InvalidDicomError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .DicomReader import DicomReader


class ReadDICOMFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ds = pydicom.dcmread(file)
        except (InvalidDicomError, Exception) as e:
            print(e)
            return Response({"error": "Invalid DICOM file"}, status=status.HTTP_400_BAD_REQUEST)

        dicom_r = DicomReader(ds=ds)
        metadata = dicom_r.get_data(
            fields=request.GET.get('fields'),
            format=request.GET.get('return_format')
        )

        return Response(metadata, status=status.HTTP_200_OK)
