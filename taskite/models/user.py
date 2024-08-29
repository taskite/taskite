import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.text import slugify

from taskite.models.base import UUIDTimestampModel


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, first_name, password):
        user = self.model(
            username=username, email=self.normalize_email(email), first_name=first_name
        )
        user.set_password(password)
        user.is_admin = True
        user.verified_at = timezone.now()
        user.save(using=self._db)

        return user


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(verified_at__isnull=False)
            .filter(restricted_at__isnull=True)
        )


class User(UUIDTimestampModel, AbstractBaseUser):
    username = models.CharField(max_length=124, unique=True, blank=True)
    email = models.CharField(max_length=124, unique=True)
    first_name = models.CharField(max_length=124)
    last_name = models.CharField(max_length=124, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="users/avatars/")

    is_password_expired = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    verified_at = models.DateTimeField(blank=True, null=True)
    restricted_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "users"

    objects = UserManager()
    active_objects = ActiveUserManager()

    def __str__(self) -> str:
        return f"{self.username} <{self.email}>"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.username:
                self.username = slugify(self.first_name) + str(random.randint(100, 999))
        return super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
