from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser with the given email and password."""
        user = self.create_user(
            email,
            password=password, **extra_fields
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class AppUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    is_admin = models.BooleanField(default=False)

    objects = AppUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        return super().save(*args, **kwargs)
