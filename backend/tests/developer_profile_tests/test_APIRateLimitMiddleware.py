import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time

from django.utils.timezone import now
from django.urls import reverse
from django.http import JsonResponse
from developer_profile.middleware import APIRateLimitMiddleware
from developer_profile.models import DeveloperActivityLog


BASE_URL = reverse('dicom_reader:read-dicom-file')
BASE_WRITE_DICOM_URL = reverse('dicom_writer:upload-content-for-dicom-image')


@pytest.mark.django_db
def test_request_below_limit(mocker, api_request_factory_with_logged_in_developer, developer_profile):
    """Test API request when under the limit."""
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)

    request = api_request_factory_with_logged_in_developer(BASE_URL)

    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b'{"success": "ok"}'

    current_month_logs = DeveloperActivityLog.objects.filter(
        developer=developer_profile.user,
        timestamp__month=now().month,
        timestamp__year=now().year
    )

    assert current_month_logs.count() == 1


@pytest.mark.django_db
def test_create_dicom_request_below_limit(mocker, api_request_factory_with_logged_in_developer, developer_profile):
    """Test API request when under the limit."""
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)

    request = api_request_factory_with_logged_in_developer(BASE_WRITE_DICOM_URL)

    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b'{"success": "ok"}'

    current_month_logs = DeveloperActivityLog.objects.filter(
        developer=developer_profile.user,
        timestamp__month=now().month,
        timestamp__year=now().year
    )

    assert current_month_logs.count() == 1


@pytest.mark.django_db
def test_request_exceeds_limit(mocker, api_request_factory_with_logged_in_developer, developer_profile):
    """Test API request when exceeding the limit."""
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)
    request = api_request_factory_with_logged_in_developer(BASE_URL)

    logs = [
        DeveloperActivityLog(
            developer=developer_profile.user,
            endpoint="read-dicom-file",
            timestamp=datetime.now()
        )
        for _ in range(1000)
    ]
    DeveloperActivityLog.objects.bulk_create(logs)

    response = middleware(request)

    assert response.status_code == 429
    assert b"Monthly API request for 'read-dicom-file' limit exceeded." in response.content

    current_month_logs = DeveloperActivityLog.objects.filter(
        developer=developer_profile.user,
        timestamp__month=now().month,
        timestamp__year=now().year
    )

    assert current_month_logs.count() == 1000


@pytest.mark.django_db
def test_reset_limit_next_month(mocker, api_request_factory_with_logged_in_developer, developer_profile):
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)
    request = api_request_factory_with_logged_in_developer(BASE_URL)

    current_date = datetime.now()
    next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    with freeze_time(current_date.replace(day=1)):
        logs = [
            DeveloperActivityLog(
                developer=developer_profile.user,
                endpoint="read-dicom-file",
                timestamp=current_date
            )
            for _ in range(1000)
        ]
        DeveloperActivityLog.objects.bulk_create(logs)

        response = middleware(request)
        assert response.status_code == 429

    with freeze_time(next_month):
        response = middleware(request)
        assert response.status_code == 200


@pytest.mark.django_db
def test_request_non_limited_endpoint(mocker, api_request_factory_with_logged_in_developer, developer_profile):
    """Test API request to an endpoint without a defined limit."""
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)

    request = api_request_factory_with_logged_in_developer(reverse('developer_profile:developer-profile'))

    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b'{"success": "ok"}'

    current_month_logs = DeveloperActivityLog.objects.filter(
        developer=developer_profile.user,
        timestamp__month=now().month,
        timestamp__year=now().year
    )
    assert current_month_logs.count() == 0


@pytest.mark.django_db
def test_unauthenticated_user(mocker, api_rf, base_app_user):
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)

    request = api_rf.get(BASE_URL)
    request.user = None

    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b'{"success": "ok"}'


@pytest.mark.django_db
def test_authenticated_non_developer(mocker, api_rf, base_app_user):
    mock_get_response = mocker.Mock(return_value=JsonResponse({"success": "ok"}))
    middleware = APIRateLimitMiddleware(mock_get_response)

    request = api_rf.get(BASE_URL)
    request.user = base_app_user
    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b'{"success": "ok"}'

    current_month_logs = DeveloperActivityLog.objects.filter(
        developer=base_app_user,
        timestamp__month=now().month,
        timestamp__year=now().year
    )

    assert current_month_logs.count() == 0
