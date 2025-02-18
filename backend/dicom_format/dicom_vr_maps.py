import pydicom
from pydicom.valuerep import DSfloat, IS, PersonName
from rest_framework import serializers


dicom_vr_to_python_type = {
    "AE": str, "AS": str, "AT": tuple, "CS": str, "DA": str,
    "DS": DSfloat,
    "DT": str, "FL": float, "FD": float,
    "IS": IS,
    "LO": str, "LT": str, "OB": bytes, "OD": bytes, "OF": bytes, "OW": bytes,
    "PN": PersonName,
    "SH": str, "SL": int, "SS": int, "ST": str, "TM": str,
    "UI": pydicom.uid.UID,
    "UL": int, "US": int, "UT": str
}


dicom_vr_to_serializer_field = {
    "AE": serializers.CharField(max_length=255),  # str -> CharField
    "AS": serializers.CharField(max_length=255),  # str -> CharField
    "AT": serializers.ListField(child=serializers.CharField(max_length=255)),  # tuple -> ListField of CharFields
    "CS": serializers.CharField(max_length=255),  # str -> CharField
    "DA": serializers.DateField(),  # str (format YYYY-MM-DD) -> DateField
    "DS": serializers.FloatField(),  # float -> FloatField
    "DT": serializers.DateTimeField(),  # str -> DateTimeField
    "FL": serializers.FloatField(),  # float -> FloatField
    "FD": serializers.FloatField(),  # float -> FloatField
    "IS": serializers.IntegerField(),  # int -> IntegerField
    "LO": serializers.CharField(max_length=255),  # str -> CharField
    "LT": serializers.CharField(max_length=255),  # str -> CharField
    "OB": serializers.FileField(),  # bytes -> FileField
    "OD": serializers.FileField(),  # bytes -> FileField
    "OF": serializers.FileField(),  # bytes -> FileField
    "OW": serializers.FileField(),  # bytes -> BytesField
    "PN": serializers.CharField(max_length=255),  # str -> CharField
    "SH": serializers.CharField(max_length=255),  # str -> CharField
    "SL": serializers.IntegerField(),  # int -> IntegerField
    "SS": serializers.IntegerField(),  # int -> IntegerField
    "ST": serializers.CharField(max_length=255),  # str -> CharField
    "TM": serializers.TimeField(),  # str (format HH:MM:SS) -> TimeField
    "UI": serializers.CharField(max_length=255),  # str -> CharField
    "UL": serializers.IntegerField(),  # int -> IntegerField
    "US": serializers.IntegerField(),  # int -> IntegerField
    "UT": serializers.CharField(max_length=255),  # str -> CharField
}
