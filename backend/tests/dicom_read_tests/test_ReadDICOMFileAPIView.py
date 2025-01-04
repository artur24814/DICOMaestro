import pytest
from io import BytesIO

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework import status

from tests.factories.dicom_files import SIMPLE_DICOM_FILE
from tests.testing_data.accounts import BASE_USER_DATA
from tests.decorators.num_queries import assert_num_queries

from helpers.loaders import FileLoader

from tests.helpers.tokens_handler import get_access_key


User = get_user_model()
BASE_URL = reverse('dicom_reader:read-dicom-file')


@pytest.mark.django_db
@assert_num_queries(0)
def test_forbidden_unauthorised_user(api_client):
    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')

    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(
            BASE_URL,
            {'file': dicom_file},
            format='multipart',
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
@assert_num_queries(3)
def test_aupload_valid_dicom_real_file_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')

    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(
            BASE_URL,
            {'file': dicom_file},
            format='multipart',
            headers=headers
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['PatientID'] == "556342B"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Modality'] == "XA"

        # Check if image data is present (base64)
        assert 'Images' in response_data


@pytest.mark.django_db
def test_aupload_valid_dicom_real_file_by_developer_user(api_client, developer_profile):
    api_client.force_authenticate(user=developer_profile.user)
    payload = {"name": "new-key"}
    response = api_client.post(reverse('developer_auth:api-key'), data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    headers = {"Authorization": f"ApiKey {response.data['api_key']}"}

    api_client.logout()
    response_logout = api_client.post(reverse('developer_auth:api-key'), data=payload)
    assert response_logout.status_code == status.HTTP_401_UNAUTHORIZED

    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        with CaptureQueriesContext(connection) as context:
            response = api_client.post(BASE_URL, {'file': dicom_file}, format='multipart', headers=headers)
            assert len(context.captured_queries) <= 5

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['PatientID'] == "556342B"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Modality'] == "XA"

        # Check if image data is present (base64)
        assert 'Images' in response_data


@pytest.mark.django_db
@assert_num_queries(3)
def test_file_upload_text_file_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    invalid_file = BytesIO(b"Invalid content")
    invalid_file.name = "invalid.txt"

    response = api_client.post(BASE_URL, {'file': invalid_file}, format='multipart', headers=headers)

    assert response.status_code == 400
    assert response.json()['file'] == ["Invalid file type. Only .dcm, .DCM, .zip are allowed."]


@pytest.mark.django_db
@assert_num_queries(3)
def test_file_upload_lack_file_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}
    response = api_client.post(BASE_URL, format='multipart', headers=headers)

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["file"] == ["This field may not be null."]


@pytest.mark.django_db
@assert_num_queries(3)
def test_upload_valid_dicom_mock_file_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}
    response = api_client.post(BASE_URL, {'file': SIMPLE_DICOM_FILE}, format='multipart', headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['PatientName'] == "John Doe"
    assert response_data['PatientID'] == "12345"
    assert response_data['StudyDate'] == "20240101"
    assert response_data['Modality'] == "CT"
    assert response_data['Manufacturer'] == "TestManufacturer"

    assert 'Images' not in response_data


@pytest.mark.django_db
@assert_num_queries(3)
def test_upload_valid_dicom_real_file_expect_GIF_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(
            BASE_URL + '?return_format=gif',
            {'file': dicom_file},
            format='multipart',
            headers=headers
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['PatientID'] == "556342B"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Modality'] == "XA"

        # Check if image data is present (base64)
        assert 'Images' in response_data
        assert isinstance(response_data['Images'][0], str)
        assert response_data['ImageFormat'] == 'GIF'


@pytest.mark.django_db
@assert_num_queries(3)
def test_upload_valid_dicom_real_file_expect_list_by_authenticated_user(api_client, base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(BASE_URL, {'file': dicom_file}, format='multipart', headers=headers)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['PatientID'] == "556342B"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Modality'] == "XA"

        # Check if image data is present (base64)
        assert 'Images' in response_data
        assert len(response_data['Images']) == 96
        assert isinstance(response_data['Images'][0], str)
        assert response_data['ImageFormat'] == 'PNG'


@pytest.mark.django_db
@assert_num_queries(3)
def test_upload_valid_dicom_real_file_with_required_specific_field_expect_list_by_authenticated_user(api_client,
                                                                                                     base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}
    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(
            BASE_URL + "?fields=Manufacturer,PatientName,StudyDate",
            {'file': dicom_file},
            format='multipart',
            headers=headers
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Manufacturer'] == ""

        assert response_data.get('PatientID') is None
        assert response_data.get('Modality') is None

        # Check if image data is present (base64)
        assert 'Images' in response_data
        assert len(response_data['Images']) == 96
        assert isinstance(response_data['Images'][0], str)
        assert response_data['ImageFormat'] == 'PNG'


@pytest.mark.django_db
@assert_num_queries(3)
def test_upload_valid_dicom_real_file_with_required_invalid_field_expect_error_by_authenticated_user(api_client,
                                                                                                     base_app_user):
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(
            BASE_URL + "?fields=Manufacturer,PatientName,StudyDate,Balabla,FakeField,Tadam",
            {'file': dicom_file},
            format='multipart',
            headers=headers
        )

        assert response.status_code == 400
        response_data = response.json()
        assert response_data['fields'] == ["Invalid fields: Balabla, FakeField, Tadam"]
