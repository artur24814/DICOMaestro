import base64
from io import BytesIO
from PIL import Image
import numpy as np
from pydicom.dataset import FileDataset


class DicomReader:
    def __init__(self, ds: FileDataset):
        self.ds = ds

    def get_data(self, fields=None, format=None) -> dict:
        data = dict()
        metadata = self.get_metadata(self.ds, fields=fields)
        images = self.get_images(self.ds, format=format)
        data.update(metadata)
        data.update(images)
        return data

    def get_metadata(self, ds: FileDataset, fields=None) -> dict:
        if fields:
            metadata = {field: str(ds.get(field, "Unknown")) for field in fields.split(',')}
        else:
            metadata = {elem.keyword: str(elem.value) for elem in ds if elem.keyword and elem.value}
        return metadata

    def get_images(self, ds: FileDataset, **kwargs) -> dict:
        image_data = dict()
        expected_format = kwargs.get('format')
        if ds.get('PixelData'):
            pixel_array = ds.pixel_array
            images_base64 = []
            if self.is_a_2D_image_or_a_singleLayer_3D_image(pixel_array):
                image_base64 = self.create_2d_image_base64(pixel_array[0])
                images_base64.append(image_base64)
                image_data['ImageFormat'] = 'PNG'
            elif self.is_a_3D_image_and_the_expected_gif_format(pixel_array, expected_format):
                image_base64 = self.create_gif_image_base64(pixel_array)
                images_base64.append(image_base64)
                image_data['ImageFormat'] = 'GIF'
            else:
                for i in range(pixel_array.shape[0]):
                    image_base64 = self.create_2d_image_base64(pixel_array[i])
                    images_base64.append(image_base64)
                image_data['ImageFormat'] = 'PNG'

            image_data['Images'] = images_base64
        return image_data

    def is_a_2D_image_or_a_singleLayer_3D_image(self, pixel_array: np.ndarray) -> bool:
        return pixel_array.ndim == 2 or (pixel_array.ndim == 3 and pixel_array.shape[0] == 1)

    def create_2d_image_base64(self, pixel_array: np.ndarray) -> BytesIO:
        img = Image.fromarray(pixel_array)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return base64.b64encode(img_byte_arr.read()).decode('utf-8')

    def is_a_3D_image_and_the_expected_gif_format(self, pixel_array: np.ndarray, expected_format: str) -> bool:
        return pixel_array.ndim == 3 and expected_format == 'gif'

    def create_gif_image_base64(self, pixel_array: np.ndarray) -> BytesIO:
        frames = [Image.fromarray(pixel_array[i]) for i in range(pixel_array.shape[0])]

        img_byte_arr = BytesIO()
        frames[0].save(
            img_byte_arr,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        img_byte_arr.seek(0)
        return base64.b64encode(img_byte_arr.read()).decode('utf-8')
