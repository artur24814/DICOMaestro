from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile
from dicom_format.utils import get_dicom_field_to_serializer_field


class DicomFileContentUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=255)
    image = serializers.ImageField()

    def __init__(self, *args, **kwargs):
        dicom_fields = kwargs.pop("dicom_fields", [])
        required_dicom_field_serializer_types = get_dicom_field_to_serializer_field()
        self.dicom_filed_names = list()
        super().__init__(*args, **kwargs)

        for dicom_field in dicom_fields:
            if dicom_field in list(required_dicom_field_serializer_types.keys()):
                self.fields[dicom_field] = required_dicom_field_serializer_types[dicom_field]
                self.dicom_filed_names.append(dicom_field)

    def validate_image(self, value: UploadedFile):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("The file is too large! Maximum size is 5MB.")

        if value.content_type not in ["image/png", "image/jpeg"]:
            raise serializers.ValidationError("Unsupported format! Allowed: PNG, JPEG.")

        return value
