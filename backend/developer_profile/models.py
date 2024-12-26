from django.db import models
from accounts.models import AppUser


class DeveloperProfile(models.Model):
    PURPOSE_CHOICES = [
        ("testing", "Building a test application"),
        ("research", "Conducting research"),
        ("education", "Learning/education"),
        ("commercial", "Commercial purposes"),
        ("other", "Other"),
    ]
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name="developer_profile")
    purpose = models.CharField(max_length=50,
                               choices=PURPOSE_CHOICES, blank=True, null=True,
                               help_text="Purpose for registering as a developer")
    organization = models.CharField(max_length=255, blank=True, null=True, help_text="Organization name, if any")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DeveloperProfile for {self.user.username}"
