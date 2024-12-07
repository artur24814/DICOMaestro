import pydicom
from pydicom.datadict import keyword_dict


def get_allowed_dicom_fields() -> set:
    return set(keyword_dict.keys())


def get_dicom_version() -> str:
    return pydicom.__version__
