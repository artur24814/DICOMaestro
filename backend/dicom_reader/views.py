import pydicom
import asyncio
from pydicom.errors import InvalidDicomError
from rest_framework import status
from adrf.views import APIView as AsyncApiView
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .DicomReader import DicomReader
from .serializers import DicomQueryParamsSerializer


class ReadDICOMFileAPIView(AsyncApiView):
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [IsAuthenticated]

    async def post(self, request, *args, **kwargs):
        serializer = DicomQueryParamsSerializer(
            data={
                **request.GET.dict(),
                'file': request.FILES.get('file')
            }
        )
        serializer.is_valid(raise_exception=True)

        fields = serializer.validated_data.get('fields')
        file = serializer.validated_data['file']
        return_format = serializer.validated_data.get('return_format')

        try:
            ds = await asyncio.to_thread(pydicom.dcmread, file)
        except (InvalidDicomError, Exception) as e:
            print(e)
            return Response({"file": ["Invalid DICOM file"]}, status=status.HTTP_400_BAD_REQUEST)

        dicom_r = DicomReader(ds=ds)
        metadata = await asyncio.to_thread(
            dicom_r.get_data,
            fields=fields,
            format=return_format
        )

        return Response(metadata, status=status.HTTP_200_OK)
