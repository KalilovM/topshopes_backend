from django.contrib.auth.hashers import make_password
from typing import Optional, Any, TypeVar
from django.contrib.auth.models import UserManager

_T = TypeVar("_T")

class CustomeManager(UserManager):
    def create_user(self, email: Optional[str] = ..., password: Optional[str] = ..., **extra_fields: Any) -> _T:
        email = self.normalize_email(email)  
        user = self.model(email=email, password=password, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user


    def create_superuser(self, email: Optional[str] = ..., password: Optional[str] = ..., **extra_fields: Any) -> _T:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        self.create_user(email=email, password=password, **extra_fields)
