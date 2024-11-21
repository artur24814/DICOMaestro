import pytest
from io import BytesIO
from django.urls import reverse
# from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()
BASE_URL = reverse('dicom_reader:read-dicom-file')


@pytest.mark.django_db
def test_file_upload_text_file(client):
    test_file = BytesIO(b"Test content")
    test_file.name = "test.txt"

    response = client.post(BASE_URL, {'file': test_file}, format='multipart')

    assert response.status_code == 200

    response_data = response.json()
    assert response_data['filename'] == "test.txt"
    assert response_data['content_type'] == "text/plain"
    assert response_data['size'] == len(b"Test content")


@pytest.mark.django_db
def test_file_upload_lack_file(client):
    response = client.post(BASE_URL, format='multipart')

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["error"] == "No file provided"
