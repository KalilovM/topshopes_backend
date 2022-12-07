from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import List
import uuid

from users.managers import CustomeManager


class Customer(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = None
    email = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    # TODO: check default value of date of birth on creation or on app start
    dateOfBirth = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = []
    objects = CustomeManager()

    def __str__(self) -> str:
        return self.email


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=35)
    street = models.CharField(max_length=55)
    phone = models.CharField(max_length=35)

    def __str__(self) -> str:
        return self.user
