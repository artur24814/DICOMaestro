import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

BASE_URL = reverse('dicom_writer:upload-content-for-dicom-image')


@pytest.mark.django_db
def test_send_content_and_response_image(api_client, mock_image):
    image_file = SimpleUploadedFile("test_image.png", mock_image.read(), content_type="image/png")

    data = {
        "file_name": "Example Title",
        "image": image_file,
    }

    response = api_client.post(BASE_URL, data, format="multipart")

    assert response.status_code == status.HTTP_200_OK
    content_disposition = response.headers.get("Content-Disposition", "")
    assert "attachment; filename=" in content_disposition
    assert response.headers.get("Content-Type") == "application/dicom"
    assert len(response.content) > 0
