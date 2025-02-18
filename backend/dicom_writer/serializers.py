from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile
from dicom_format.utils import get_dicom_field_to_serializer_field


class DicomFileContentUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=255)
    image = serializers.ImageField()

    def __init__(self, *args, **kwargs):
        dicom_fields = kwargs.pop("dicom_fields", [])
        required_dicom_field_serializer_types = get_dicom_field_to_serializer_field()
        self.dicom_field_serializators = dict()
        super().__init__(*args, **kwargs)

        for dicom_field in dicom_fields:
            if dicom_field in list(required_dicom_field_serializer_types.keys()):
                serializing_field = required_dicom_field_serializer_types[dicom_field]
                self.dicom_field_serializators[dicom_field] = (serializing_field, kwargs['data'].pop(dicom_field))

    def validate(self, attrs):
        for dicom_field, data in self.dicom_field_serializators.items():
            try:
                data[0].run_validation(data[1][0])
            except serializers.ValidationError as e:
                raise serializers.ValidationError(f'{dicom_field}: {e.detail[0]}')
        return super().validate(attrs)

    def validate_image(self, value: UploadedFile):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("The file is too large! Maximum size is 5MB.")

        if value.content_type not in ["image/png", "image/jpeg"]:
            raise serializers.ValidationError("Unsupported format! Allowed: PNG, JPEG.")

        return value
