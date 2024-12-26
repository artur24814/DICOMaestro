from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import DeveloperAPIKey


class HasDeveloperAPIKey(BaseHasAPIKey):
    model = DeveloperAPIKey
