from io import BytesIO

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse

from .serializers import DicomFileContentUploadSerializer
from .dicom_file_factory import CustomeDicomFileFactory


class DicomFileDataSetUploadAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DicomFileContentUploadSerializer(data=request.data, dicom_fields=list(request.data.keys()))

        if serializer.is_valid():
            uploaded_image = request.FILES.get("image")
            file_name = serializer.validated_data.get('file_name')
            image_bytes = BytesIO(uploaded_image.read())
            dicom_file_factory = CustomeDicomFileFactory()
            dicom_file = dicom_file_factory.generate_dicom_file(
                file_name=f"{file_name}.dcm",
                meta_data={
                    dicom_field: data[1]
                    for dicom_field, data in serializer.dicom_field_serializators.items()
                },
                image_path=image_bytes
            )
            response = HttpResponse(dicom_file.file.getvalue(), content_type="application/dicom")
            response["Content-Disposition"] = f'attachment; filename="{file_name}.dcm"'
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
