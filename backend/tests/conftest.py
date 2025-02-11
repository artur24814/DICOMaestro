import pytest
from PIL import Image
from io import BytesIO

from rest_framework.test import APIClient, APIRequestFactory
from django.test import Client
from django.utils.timezone import now

from accounts.models import AppUser
from developer_auth.models import DeveloperAPIKey
from developer_profile.models import DeveloperProfile, DeveloperActivityLog
from dicom_writer.dicom_file_factory import CustomeDicomFileFactory

from .testing_data.accounts import BASE_USER_DATA
from .testing_data.developer_profile import DEVELOPER_USER_DATA, DEVELOPER_PROFILE_DATA


@pytest.fixture
def api_rf():
    return APIRequestFactory()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def base_app_user():
    user = AppUser.objects.create_user(
        **BASE_USER_DATA
    )
    return user


@pytest.fixture
def developer_app_user():
    user = AppUser.objects.create_user(
        **DEVELOPER_USER_DATA
    )
    return user


@pytest.fixture
def developer_profile(developer_app_user):
    profile = DeveloperProfile.objects.prefetch_related("user").create(
        user=developer_app_user,
        **DEVELOPER_PROFILE_DATA
    )
    return profile


@pytest.fixture
def activity_logs(developer_app_user):
    logs = [
        DeveloperActivityLog(
            developer=developer_app_user,
            endpoint="test-endpoint",
            timestamp=now(),
        )
        for _ in range(1, 6)
    ]
    DeveloperActivityLog.objects.bulk_create(logs)


@pytest.fixture
def api_request_factory_with_logged_in_developer(rf, developer_profile):
    """Fixture to create API requests."""
    user = developer_profile.user

    def create_request(path):
        request = rf.get(path)
        request.user = user
        return request

    return create_request


@pytest.fixture
def api_key(developer_app_user):
    key_name = "test-key"
    api_key, _ = DeveloperAPIKey.objects.create_key(name=key_name, user=developer_app_user)
    return api_key


@pytest.fixture
def dicom_factory():
    return CustomeDicomFileFactory()


@pytest.fixture
def sample_meta_data():
    return {
        "PatientName": "Test Patient",
        "PatientID": "123456",
        "StudyDescription": "Test Study"
    }


@pytest.fixture
def mock_image():
    image = Image.new("L", (128, 128), color=255)
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes
