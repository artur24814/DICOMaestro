from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializers import DeveloperProfileSerializer, DeveloperActivityLogSerializer
from .models import DeveloperProfile, DeveloperActivityLog
from .permissions import IsDeveloper
from .filters import DeveloperActivityLogFilter


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


class DeveloperActivitySummaryView(ListAPIView):
    queryset = DeveloperActivityLog.objects.all()
    permission_classes = [IsAuthenticated, IsDeveloper]
    serializer_class = DeveloperActivityLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeveloperActivityLogFilter

    def get_queryset(self):
        logs = super().get_queryset().filter(developer=self.request.user)
        logs = self.filter_queryset(logs)

        daily_summary = logs.annotate(day=TruncDate("timestamp")).values("day").annotate(count=Count("id"))
        self.monthly_total = logs.aggregate(monthly_total=Count("id"))["monthly_total"] or 0
        return daily_summary

    def list(self, request, *args, **kwargs):
        daily_summary = self.get_queryset()
        return Response({
            "daily_activity": list(daily_summary),
            "monthly_total": self.monthly_total,
        })
