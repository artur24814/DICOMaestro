from io import BytesIO
import pydicom
from pydicom.dataset import FileMetaDataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid, SecondaryCaptureImageStorage


def get_simple_dicom_mock_file(file_name: str) -> BytesIO:
    meta = FileMetaDataset()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian
    meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    meta.MediaStorageSOPInstanceUID = generate_uid()

    ds = FileDataset(file_name, {}, file_meta=meta, preamble=b"\0" * 128)
    ds.PatientName = "John Doe"
    ds.PatientID = "12345"
    ds.StudyDate = "20240101"
    ds.Modality = "CT"
    ds.Manufacturer = "TestManufacturer"
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.SOPClassUID = SecondaryCaptureImageStorage

    dicom_file = BytesIO()
    dicom_file.name = file_name

    pydicom.dcmwrite(dicom_file, ds)

    dicom_file.seek(0)
    return dicom_file


SIMPLE_DICOM_FILE = get_simple_dicom_mock_file("test.dcm")
