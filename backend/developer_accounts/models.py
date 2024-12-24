from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_api_key.models import AbstractAPIKey

User = get_user_model()


class DeveloperAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="developer_api_keys",
        help_text="The user this API key is associated with."
    )
