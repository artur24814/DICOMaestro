from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import views, status
from rest_framework.response import Response
from django.core.files.base import ContentFile

from .serializers import DicomFileContentUploadSerializer


class DicomFileDataSetUploadAPIView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DicomFileContentUploadSerializer(data=request.data, dicom_fields=list(request.data.keys()))
        if serializer.is_valid():
            uploaded_image = request.FILES.get("image")
            response_file = ContentFile(uploaded_image.read(), name=uploaded_image.name)

            response = Response(status=status.HTTP_201_CREATED)
            response["Content-Disposition"] = f'attachment; filename="{uploaded_image.name}"'
            response["Content-Type"] = uploaded_image.content_type
            response.content = response_file.read()

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
