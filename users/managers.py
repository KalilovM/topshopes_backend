from django.contrib.auth.hashers import make_password
from typing import Optional, Any
from django.contrib.auth.models import UserManager

from users.models import Customer


class CustomeManager(UserManager):
    """
    Custom manager to create custom user and superuser
    """

    def create_user(
        self,
        email: Optional[str] = ...,
        password: Optional[str] = ...,
        **extra_fields: Any
    ) -> Customer:
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email: Optional[str] = ...,
        password: Optional[str] = ...,
        **extra_fields: Any
    ) -> None:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        self.create_user(email=email, password=password, **extra_fields)
