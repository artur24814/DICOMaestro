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

        response_data = {
            "filename": file.name,
            "content_type": file.content_type,
            "size": file.size,
        }
        return Response(response_data, status=status.HTTP_200_OK)
