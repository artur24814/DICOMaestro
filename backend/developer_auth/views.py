from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from developer_profile.permissions import IsDeveloper
from .models import DeveloperAPIKey
from .serializers import DeveloperApiKeySerializer, CreateDeveloperApiKeySerializer


class DeveloperApiKeyAPIView(ListCreateAPIView, DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsDeveloper]
    serializer_class = DeveloperApiKeySerializer

    def get_queryset(self):
        return DeveloperAPIKey.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    def create(self, request, *args, **kwargs) -> Response:
        serializer = CreateDeveloperApiKeySerializer(data=request.data, context={"request": request})
        serializer.is_valid()
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        obj = self.get_object()
        self.perform_destroy(obj)
        return Response({"detail": "Key deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
