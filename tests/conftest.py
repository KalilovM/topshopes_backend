import pytest
from faker import Faker
from rest_framework.test import APIClient

from users.models import Customer


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user():
    return Customer.objects.create_user("marlen@gmail.com", "jfmfn123")
