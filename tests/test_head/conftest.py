from io import BytesIO, StringIO
from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from model_bakery import baker
from shops.models import Category, Color, Size, Product, Brand, Shop, BrandType
from tests.factories import (
    BrandFactory,
    BrandTypeFactory,
    CategoryFactory,
    ProductFactory,
    ShopFactory,
)

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
        dict(
            name="category1",
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
            description="description1",
        ),
        dict(
            name="category2",
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
            description="description2",
        ),
        dict(
            name="category3",
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
            description="description3",
        ),
    ]
    for payload in payload_set:
        admin_client.post("/api/admin/categories/", payload)
    return Category.objects.all()


@pytest.fixture
def size_set(db, admin_client: APIClient) -> List[Size]:
    size_set = baker.make(Size, _quantity=5)
    return size_set


@pytest.fixture
def color_set(db, admin_client: APIClient) -> List[Color]:
    color_set = baker.make(Color, _quantity=4)
    return color_set


@pytest.fixture
def brandtype_set(db, admin_client: APIClient) -> BrandType:
    brand_type = BrandTypeFactory.create(name="testBrandType")
    return brand_type


@pytest.fixture
def brand_set(db, admin_client: APIClient, brandtype_set) -> Brand:
    brand = BrandFactory.create(
        name="testBrand",
        type=brandtype_set,
        featured=True,
        image=InMemoryUploadedFile(
            file=StringIO("test"),
            field_name="test",
            name="test.jpg",
            content_type="image/jpeg",
            size=1,
            charset="utf-8",
        ),
    )
    return brand


@pytest.fixture
def shop_set(db, admin_client: APIClient) -> Shop:
    shop = ShopFactory.create(
        name="Testing Shop",
        user=Customer.objects.first(),
        email="testing@me.com",
        address="testingaddresss",
        verified=False,
        phone="01020304",
    )
    return shop
