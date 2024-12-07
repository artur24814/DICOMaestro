import re
from rest_framework import serializers


class DicomAllowedFieldsFilterQueryParamsSerializer(serializers.Serializer):
    fields__contains = serializers.CharField(required=False, allow_blank=True)
    fields__startswith = serializers.CharField(required=False, allow_blank=True)
    fields__endswith = serializers.CharField(required=False, allow_blank=True)
    fields__regex = serializers.CharField(required=False, allow_blank=True)

    def validate_fields__regex(self, value):
        try:
            re.compile(value)
        except re.error as e:
            raise serializers.ValidationError(f"Invalid regex pattern: {str(e)}")
        return value

    def get_patterns(self) -> list:
        patterns = []
        if self.validated_data.get("fields__contains"):
            patterns.append(f".*{re.escape(self.validated_data['fields__contains'])}.*")
        if self.validated_data.get("fields__startswith"):
            patterns.append(f"^{re.escape(self.validated_data['fields__startswith'])}.*")
        if self.validated_data.get("fields__endswith"):
            patterns.append(f".*{re.escape(self.validated_data['fields__endswith'])}$")
        if self.validated_data.get("fields__regex"):
            patterns.append(self.validated_data["fields__regex"])
        return patterns
