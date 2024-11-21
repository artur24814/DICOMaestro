import pytest
from io import BytesIO

from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.factories.dicom_files import SIMPLE_DICOM_FILE

from helpers.loaders import FileLoader

User = get_user_model()
BASE_URL = reverse('dicom_reader:read-dicom-file')


@pytest.mark.django_db
def test_file_upload_text_file(api_client):
    invalid_file = BytesIO(b"Invalid content")
    invalid_file.name = "invalid.txt"

    response = api_client.post(BASE_URL, {'file': invalid_file}, format='multipart')

    assert response.status_code == 400
    assert "Invalid DICOM file" in response.json()['error']


@pytest.mark.django_db
def test_file_upload_lack_file(api_client):
    response = api_client.post(BASE_URL, format='multipart')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["error"] == "No file provided"


@pytest.mark.django_db
def test_upload_valid_dicom_mock_file(api_client):
    response = api_client.post(BASE_URL, {'file': SIMPLE_DICOM_FILE}, format='multipart')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['PatientName'] == "John Doe"
    assert response_data['PatientID'] == "12345"
    assert response_data['StudyDate'] == "20240101"
    assert response_data['Modality'] == "CT"
    assert response_data['Manufacturer'] == "TestManufacturer"


@pytest.mark.django_db
def test_upload_valid_dicom_real_file(api_client):
    # File source -> https://www.rubomedical.com/dicom_files/
    file_path = FileLoader.load_file('tests/testing_files/dicom/0002.DCM')
    with open(file_path, 'rb') as dicom_file:
        response = api_client.post(BASE_URL, {'file': dicom_file}, format='multipart')

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['PatientName'] == "Rubo DEMO"
        assert response_data['PatientID'] == "556342B"
        assert response_data['StudyDate'] == "19941013"
        assert response_data['Modality'] == "XA"
        assert response_data['Manufacturer'] == ""
