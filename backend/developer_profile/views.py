from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializers import DeveloperProfileSerializer
from .models import DeveloperProfile


class RetreveCreateDeveloperProfileAPIView(CreateAPIView, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperProfileSerializer

    def perform_create(self, serializer):
        DeveloperProfile.objects.update_or_create(user=self.request.user, defaults=serializer.validated_data)

    def get(self, request, *args, **kwargs):
        try:
            profile = DeveloperProfile.objects.select_related('user').get(user=request.user)
        except DeveloperProfile.DoesNotExist:
            raise NotFound("Developer profile does not exist.")

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
