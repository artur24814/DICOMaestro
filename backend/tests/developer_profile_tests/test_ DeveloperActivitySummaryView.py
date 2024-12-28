import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.urls import reverse
from django.utils.timezone import now
from developer_profile.models import DeveloperActivityLog
from tests.decorators.num_queries import assert_num_queries


BASE_URL = reverse('developer_profile:activity-summary')


@pytest.mark.django_db
@assert_num_queries(4)
def test_activity_summary_default_filter(api_client, developer_profile, activity_logs):
    api_client.force_authenticate(user=developer_profile.user)

    assert len(DeveloperActivityLog.objects.all()) == 5

    response = api_client.get(BASE_URL)

    assert response.status_code == 200
    data = response.json()

    assert data["daily_activity"][0]['count'] == 5
    assert data["daily_activity"][0]['day'] == datetime.now().strftime("%Y-%m-%d")
    assert data["monthly_total"] == 5


@pytest.mark.django_db
@assert_num_queries(3)
def test_activity_summary_with_filters(api_client, developer_profile, activity_logs):
    api_client.force_authenticate(user=developer_profile.user)

    current_year = now().year
    current_month = now().month
    response = api_client.get(BASE_URL, {"timestamp__year": current_year, "timestamp__month": current_month})

    assert response.status_code == 200
    data = response.json()

    assert data["daily_activity"][0]['count'] == 5
    assert data["daily_activity"][0]['day'] == datetime.now().strftime("%Y-%m-%d")
    assert data["monthly_total"] == 5


@pytest.mark.django_db
@assert_num_queries(3)
def test_activity_summary_no_logs(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    response = api_client.get(BASE_URL)

    assert response.status_code == 200
    data = response.json()

    assert len(data["daily_activity"]) == 0
    assert data["monthly_total"] == 0


@pytest.mark.django_db
def test_activity_summary_different_month(api_client, developer_profile, activity_logs):
    api_client.force_authenticate(user=developer_profile.user)

    today = datetime.today()
    previous_month = today - relativedelta(months=1)

    record = DeveloperActivityLog.objects.create(
        developer=developer_profile.user,
        endpoint="test-endpoint",
    )
    record.timestamp = previous_month
    record.save()

    response = api_client.get(BASE_URL, {
        "timestamp__month": previous_month.month,
    })

    assert response.status_code == 200
    data = response.json()

    assert data["daily_activity"][0]["count"] == 1
    assert data["daily_activity"][0]["day"] == previous_month.strftime("%Y-%m-%d")
    assert data["monthly_total"] == 1
