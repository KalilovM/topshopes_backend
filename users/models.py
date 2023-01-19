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
    phone = models.CharField(max_length=30)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = []
    objects = CustomManager()

    def __str__(self) -> str:
        return self.email


class Application(models.Model):
    """
    Request model
    """
    REGISTRATION_CHOICES = (
        ("with_nds", "with NDS"),
        ("without_nds", "without NDS"),
    )
    STATUSES = (
        ("moderation", "moderation"),
        ("approved", "approved"),
        ("rejected", "rejected"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    document = models.FileField(upload_to=PathAndRename("documents/"))
    INN = models.CharField(max_length=14, null=True, blank=False)
    short_name = models.CharField(max_length=30, null=True, blank=False)
    full_name = models.CharField(max_length=200, null=True, blank=False)
    registration_form = models.CharField(max_length=20, choices=REGISTRATION_CHOICES,default="with_nds", null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    owner = models.CharField(max_length=100, null=True, blank=False)
    bank_account = models.CharField(max_length=16, null=True, blank=False)
    bik = models.CharField(max_length=9, null=True, blank=False)
    shop_name = models.CharField(max_length=100, null=True, blank=False)
    status = models.CharField(max_length=20, choices=STATUSES, null=True, blank=False, default="moderation")
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="application"
    )

    def __str__(self) -> str:
        return self.short_name


class Seller(models.Model):
    """
    Seller model
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    roles = models.ManyToManyField(to="roles.Role", related_name="users")
    verified = models.BooleanField(default=False)


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
