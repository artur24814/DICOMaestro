from io import BytesIO
from PIL import Image
import numpy as np

from pydicom.dataset import FileDataset
from pydicom.uid import generate_uid
from pydicom.uid import SecondaryCaptureImageStorage


class CustomeDicomFile:
    def __init__(self, file_ds: FileDataset, rgb_image_path: str):
        self._file_ds = self._init_ds(file_ds, rgb_image_path)

    def _init_ds(self, file_ds: FileDataset, rgb_image_path: str) -> FileDataset:
        ds = self.file_data_set_preprocessing(file_ds)
        ds = self.append_rgb_image_into_data_set(ds, rgb_image_path)
        return ds

    def file_data_set_preprocessing(self, file_ds: FileDataset) -> FileDataset:
        file_ds.SOPInstanceUID = generate_uid()
        file_ds.StudyInstanceUID = generate_uid()
        file_ds.SOPClassUID = SecondaryCaptureImageStorage
        file_ds.SeriesInstanceUID = generate_uid()
        return file_ds

    def append_rgb_image_into_data_set(self, file_ds: FileDataset, image_path: str) -> FileDataset:
        with open(image_path, 'rb') as f:
            image = Image.open(f)
            image = image.convert("L")
            image_data = np.array(image, dtype=np.uint8)

            if len(image_data.shape) == 2:  # Grayscale
                file_ds.Rows, file_ds.Columns = image_data.shape
                file_ds.SamplesPerPixel = 1
            elif len(image_data.shape) == 3:  # RGB or RGBA
                file_ds.Rows, file_ds.Columns, _ = image_data.shape
                file_ds.SamplesPerPixel = 3
            else:
                raise ValueError(f"Unsupported image format: {image_data.shape}")

            file_ds.BitsAllocated = 8
            file_ds.BitsStored = 8
            file_ds.HighBit = 7
            file_ds.PixelData = image_data.tobytes()
            file_ds.PhotometricInterpretation = "MONOCHROME2" if file_ds.SamplesPerPixel == 1 else "RGB"
            file_ds.PixelRepresentation = 0
            file_ds.RescaleSlope = 1.0
            file_ds.RescaleIntercept = 0.0

            return file_ds

    @property
    def ds(self) -> FileDataset:
        return self._file_ds

    @property
    def file(self) -> BytesIO:
        stream = BytesIO()
        self.ds.save_as(stream)
        stream.seek(0)

        return stream
