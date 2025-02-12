from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import views, status
from rest_framework.response import Response
from django.core.files.base import ContentFile


class DicomFileDataSetContentUploadAPIView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploaded_image = request.FILES.get("image")
        response_file = ContentFile(uploaded_image.read(), name=uploaded_image.name)

        response = Response(status=status.HTTP_201_CREATED)
        response["Content-Disposition"] = f'attachment; filename="{uploaded_image.name}"'
        response["Content-Type"] = uploaded_image.content_type
        response.content = response_file.read()

        return response
