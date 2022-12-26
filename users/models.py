import uuid
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.helpers import PathAndRename
from users.managers import CustomManager


class Customer(AbstractUser):
    """
    Custom user model
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = None
    email = models.EmailField(max_length=100, unique=True)
    avatar = models.ImageField(
        upload_to=PathAndRename("avatars/"), null=True, blank=True
    )
    roles = models.ManyToManyField(to="roles.Roles", related_name="users")
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = []
    objects = CustomManager()

    def __str__(self) -> str:
        return self.email


class Address(models.Model):
    """
    User's addresses
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        to=Customer, on_delete=models.CASCADE, related_name="addresses"
    )
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=35)
    street = models.CharField(max_length=55)
    phone = models.CharField(max_length=35)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.street}"
