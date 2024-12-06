import os
from rest_framework import serializers


class DicomQueryParamsSerializer(serializers.Serializer):
    fields = serializers.CharField(required=False, allow_blank=True)
    return_format = serializers.ChoiceField(choices=["gif", "png", "jpeg"], required=False)
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        valid_extensions = ['.dcm', '.DCM', '.zip']
        file_extension = os.path.splitext(value.name)[1].lower()

        if file_extension not in valid_extensions:
            raise serializers.ValidationError(
                f"Invalid file type. Only {', '.join(valid_extensions)} are allowed."
            )

        return value

    def validate_fields(self, value):
        if value:
            try:
                field_list = value[0].split(",")
                if not all(field_list):
                    raise serializers.ValidationError("Fields contain empty values.")
            except Exception as e:
                raise serializers.ValidationError(
                    "Invalid format for fields. Should be: field,field,..."
                ) from e
        return value

    def validate_return_format(self, value):
        if value and value not in ["gif", "png", "jpeg"]:
            raise serializers.ValidationError(f"'{value}' is not a valid choice.")
        return value
