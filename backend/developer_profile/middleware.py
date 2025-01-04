from django.http import JsonResponse
from django.urls import resolve
from django.utils.timezone import now
from .models import DeveloperActivityLog
from accounts.models import AppUser


class APIRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.endpoint_limits = {
            'read-dicom-file': 1000,
        }

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        if not user or not user.is_authenticated:
            return response

        endpoint_name = self.get_endpoint_name(request)

        if endpoint_name in self.endpoint_limits.keys() and user.is_developer:
            requests_used = self.count_current_month_logs(endpoint_name, user)
            endpoint_limit = self.endpoint_limits[endpoint_name]

            if requests_used >= endpoint_limit:
                return JsonResponse({
                    "error": f"Monthly API request for '{endpoint_name}' limit exceeded.",
                    "quota": endpoint_limit,
                    "requests_used": requests_used,
                }, status=429)

            DeveloperActivityLog.objects.create(developer=user, endpoint=endpoint_name)
        return response

    def get_endpoint_name(self, request):
        resolved_url = resolve(request.path_info)
        return resolved_url.url_name

    def count_current_month_logs(self, endpoint: str, user: AppUser) -> int:
        current_month_logs = DeveloperActivityLog.objects.filter(
            developer=user,
            endpoint=endpoint,
            timestamp__month=now().month,
            timestamp__year=now().year
        )
        return current_month_logs.count()
