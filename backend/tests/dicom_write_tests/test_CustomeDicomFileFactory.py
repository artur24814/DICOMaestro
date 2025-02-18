from io import BytesIO
from PIL import Image

from pydicom.uid import ExplicitVRLittleEndian


def test_generate_dicom_file(dicom_factory, sample_meta_data, mock_image):
    dicom_f = dicom_factory.generate_dicom_file("test.dcm", sample_meta_data, mock_image)
    dicom_stream = dicom_f.file

    assert isinstance(dicom_stream, BytesIO)

    dicom_ds = dicom_f.ds

    assert dicom_ds.file_meta.TransferSyntaxUID == ExplicitVRLittleEndian
    assert dicom_ds.PatientName == "Test Patient"
    assert dicom_ds.PatientID == "123456"
