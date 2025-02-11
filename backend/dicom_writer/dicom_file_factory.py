from pydicom.uid import ExplicitVRLittleEndian
from pydicom.uid import SecondaryCaptureImageStorage
from pydicom.uid import generate_uid
from pydicom.dataset import FileMetaDataset, FileDataset, Dataset

from .dicom_file import CustomeDicomFile


class CustomeDicomFileFactory:

    def generate_dicom_file(self, file_name: str, meta_data: dict, image_path: str) -> CustomeDicomFile:
        ds = self._get_data_set(meta_data)
        file_meta_ds = self._get_file_meta_dataset()
        file_ds = self._get_file_data_set(file_name, ds, file_meta_ds)
        return self._get_dicom_file(file_ds, image_path)

    def _get_data_set(self, meta_data: dict) -> Dataset:
        ds = Dataset()
        for key, value in meta_data.items():
            setattr(ds, key, value)
        return ds

    def _get_file_meta_dataset(self) -> FileMetaDataset:
        file_meta_ds = FileMetaDataset()
        file_meta_ds.TransferSyntaxUID = ExplicitVRLittleEndian
        file_meta_ds.MediaStorageSOPInstanceUID = generate_uid()
        file_meta_ds.MediaStorageSOPInstanceUID = SecondaryCaptureImageStorage
        return file_meta_ds

    def _get_file_data_set(self, file_name: str, ds: Dataset, file_meta_ds: FileMetaDataset) -> FileDataset:
        return FileDataset(file_name, dataset=ds, file_meta=file_meta_ds, preamble=b"\0" * 128)

    def _get_dicom_file(self, file_ds: FileDataset, image_path: str) -> CustomeDicomFile:
        return CustomeDicomFile(file_ds=file_ds, rgb_image_path=image_path)
