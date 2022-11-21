from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Customer(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    dateOfBirth = models.DateField()
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    is_seller = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(to=Customer, on_delete=models.SET_NULL)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=35)
    street = models.CharField(max_length=55)
    phone = models.CharField(max_length=35)

    def __str__(self) -> str:
        return self.user.username
