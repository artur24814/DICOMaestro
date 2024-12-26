from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import DeveloperProfile


@receiver(post_save, sender=DeveloperProfile)
def add_developer_to_group(sender, instance, created, **kwargs):
    if created:
        developer_group, _ = Group.objects.get_or_create(name="Developer")
        instance.user.groups.add(developer_group)
