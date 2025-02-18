import pytest
from io import BytesIO
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from tests.helpers.tokens_handler import get_access_key
from tests.testing_data.accounts import BASE_USER_DATA
from tests.decorators.num_queries import assert_num_queries


BASE_URL = reverse('dicom_writer:upload-content-for-dicom-image')
BASE_READ_URL = reverse('dicom_reader:read-dicom-file')


@pytest.mark.django_db
@assert_num_queries(0)
def test_send_content_and_response_image(api_client, mock_image, base_app_user):
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


@pytest.mark.django_db
@assert_num_queries(3)
def test_send_content_and_read_file_after_response(api_client, mock_image, base_app_user):
    image_file = SimpleUploadedFile("test_image.png", mock_image.read(), content_type="image/png")

    data = {
        "file_name": "Example Title",
        "image": image_file,
        "PatientName": "TEST Name",
        "PatientID": "12345B",
        "StudyDate": "20241013",
        "Modality": "XA"
    }

    response = api_client.post(BASE_URL, data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    # open file and read it -----------------------------------------
    access_key = get_access_key(api_client, BASE_USER_DATA)
    headers = {"Authorization": f"Bearer {access_key}"}

    dicom_bytes = BytesIO(response.content)
    dicom_file = SimpleUploadedFile("output.dcm", dicom_bytes.getvalue(), content_type="application/dicom")

    response_read = api_client.post(
        BASE_READ_URL,
        {'file': dicom_file},
        format='multipart',
        headers=headers
    )

    assert response_read.status_code == 200
    response_read_data = response_read.json()
    assert response_read_data['PatientName'] == "TEST Name"
    assert response_read_data['PatientID'] == "12345B"
    assert response_read_data['StudyDate'] == "20241013"
    assert response_read_data['Modality'] == "XA"

    # Check if image data is present (base64)
    assert 'Images' in response_read_data


@pytest.mark.django_db
@assert_num_queries(0)
def test_send_content_with_unvalid_fileds_data_types_str_instead_of_float(api_client, mock_image, base_app_user):
    image_file = SimpleUploadedFile("test_image.png", mock_image.read(), content_type="image/png")

    data = {
        "file_name": "Example Title",
        "image": image_file,
        "PatientSize": "error",  # Must be float
        "PatientID": "12345B",
        "StudyDate": "20241013",
        "Modality": "XA"
    }

    response = api_client.post(BASE_URL, data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0] == 'PatientSize: A valid number is required.'


@pytest.mark.django_db
@assert_num_queries(0)
def test_send_content_with_unvalid_fileds_data_types_str_instead_of_bytes(api_client, mock_image, base_app_user):
    image_file = SimpleUploadedFile("test_image.png", mock_image.read(), content_type="image/png")

    data = {
        "file_name": "Example Title",
        "image": image_file,
        "CoordinateSystemAxisValues": "error",  # Must be bytes
        "PatientID": "12345B",
        "StudyDate": "20241013",
        "Modality": "XA"
    }

    response = api_client.post(BASE_URL, data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0] == 'CoordinateSystemAxisValues: The submitted data was not a file. '\
        'Check the encoding type on the form.'
