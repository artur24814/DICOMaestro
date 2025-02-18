import pydicom
from pydicom.datadict import keyword_dict, dictionary_VR
from .dicom_vr_maps import dicom_vr_to_python_type, dicom_vr_to_serializer_field


def get_allowed_dicom_fields() -> set:
    return set(keyword_dict.keys())


def get_dicom_field_to_python_types() -> dict:
    all_tags = keyword_dict.keys()
    field_types = {tag: str(dicom_vr_to_python_type.get(dictionary_VR(tag), str)) for tag in all_tags}
    return field_types


def get_dicom_field_to_serializer_field() -> dict:
    all_tags = keyword_dict.keys()
    field_types = {tag: dicom_vr_to_serializer_field.get(dictionary_VR(tag), str) for tag in all_tags}
    return field_types


def get_dicom_version() -> str:
    return pydicom.__version__
