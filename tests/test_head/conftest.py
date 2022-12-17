from io import BytesIO, StringIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from rest_framework.response import Response
from rest_framework.test import APIClient

from users.models import Customer


@pytest.fixture
def admin_tokens(client: APIClient, db) -> Response:
    Customer.objects.create_superuser("admin", "admin")
    admin_data = dict(email="admin", password="admin")
    tokens_data: Response = client.post("/api/auth/login/", admin_data)
    return tokens_data


@pytest.fixture
def admin_client(admin_tokens: Response, client: APIClient) -> APIClient:
    client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_tokens.data["access"])
    return client


@pytest.fixture
def category_set(db, admin_client: APIClient):
    # upload a valid image error in test

    payload_set = [
        dict(name="category1", image=SimpleUploadedFile(
            name="test_image.jpg",
            content=open("tests/test_head/testimage.webp", "rb").read(),
            content_type="image/jpeg",
        ),
             description="description1"),
        dict(name="category2", image=SimpleUploadedFile(
            name="test_image.jpg",
            content=open("tests/test_head/testimage.webp", "rb").read(),
            content_type="image/jpeg",
        ),
             description="description2"),
        dict(name="category3", image=SimpleUploadedFile(
            name="test_image.jpg",
            content=open("tests/test_head/testimage.webp", "rb").read(),
            content_type="image/jpeg",
        ),
             description="description3"),
    ]
    for payload in payload_set:
        response = admin_client.post("/api/admin/categories/", payload)
