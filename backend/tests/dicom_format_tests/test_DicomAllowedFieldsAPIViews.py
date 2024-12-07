import pytest
from django.urls import reverse

from tests.decorators.num_queries import assert_num_queries


BASE_URL = reverse('dicom_format:allowed-fields')


@pytest.mark.django_db
@assert_num_queries(0)
def test_get_allowed_dicom_fields_without_args(api_client):
    response = api_client.get(BASE_URL)

    assert response.status_code == 200
    response_data = response.json()
    assert "allowedFields" in response_data
    assert "dicomVersion" in response_data


@pytest.mark.django_db
@assert_num_queries(0)
def test_get_allowed_dicom_fields_contains_arg(api_client):
    response = api_client.get(BASE_URL + '?fields__contains=PatientSex')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("allowedFields").sort() == ["PatientSex", "PatientSexNeutered"].sort()


@pytest.mark.django_db
@assert_num_queries(0)
def test_get_allowed_dicom_fields_startswith_arg(api_client):
    response = api_client.get(BASE_URL + '?fields__startswith=StudyDate')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("allowedFields") == ["StudyDate"]


@pytest.mark.django_db
@assert_num_queries(0)
def test_get_allowed_dicom_fields_endswith_arg(api_client):
    response = api_client.get(BASE_URL + '?fields__endswith=Patient')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("allowedFields").sort() == [
        "ColumnAngulationPatient",
        "DataCollectionCenterPatient",
        "ImagePositionPatient",
        "CalciumScoringMassFactorPatient",
        "ReconstructionTargetCenterPatient",
        "ImageOrientationPatient",
        "DistanceSourceToPatient"
    ].sort()


@pytest.mark.django_db
@assert_num_queries(0)
def test_get_allowed_dicom_fields_regex_arg(api_client):
    response = api_client.get(BASE_URL + '?fields__regex=^StudyDate.*')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("allowedFields") == ["StudyDate"]
