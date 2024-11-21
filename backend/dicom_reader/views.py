import pydicom
from pydicom.errors import InvalidDicomError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class ReadDICOMFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dicom_file = pydicom.dcmread(file, stop_before_pixels=True)
        except (InvalidDicomError, Exception) as e:
            print(e)
            return Response({"error": "Invalid DICOM file"}, status=status.HTTP_400_BAD_REQUEST)

        metadata = {
            "PatientName": str(dicom_file.get("PatientName", "Unknown")),
            "PatientID": str(dicom_file.get("PatientID", "Unknown")),
            "StudyDate": str(dicom_file.get("StudyDate", "Unknown")),
            "Modality": str(dicom_file.get("Modality", "Unknown")),
            "Manufacturer": str(dicom_file.get("Manufacturer", "Unknown")),
        }

        return Response(metadata, status=status.HTTP_200_OK)
