from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import DeveloperProfile


@receiver(post_save, sender=DeveloperProfile)
def add_developer_to_group(sender, instance: DeveloperProfile, created: bool, **kwargs) -> None:
    """
    TODO: In future using cache:
    group = cache.get('developer_group')
    if not group:
        group, _ = Group.objects.get_or_create(name="Developer")
        cache.set('developer_group', group, timeout=3600)  # Cache for 1 hour
    return group
    """
    if created:
        developer_group, _ = Group.objects.get_or_create(name="Developer")
        instance.user.groups.add(developer_group)
