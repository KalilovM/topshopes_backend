import json
from io import StringIO
from typing import List

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from model_bakery import baker
from rest_framework.response import Response
from rest_framework.test import APIClient

import shops.models
from shops.models import Size, Color, Category
from tests.factories import BrandFactory, BrandTypeFactory, ShopFactory, ProductFactory, CategoryFactory
from users.models import Customer

pytestmark = pytest.mark.django_db


class TestAdminUserViewset:
    """
    Test /api/admin/users/
    """

    # TODO: About admin creation

    endpoint = "/api/admin/users/"
    payload = dict(
        email="test@gmail.com",
        phone="09090909",
        password="jfmnf123"
    )

    def test_permission_any_failed(self, client: APIClient):
        response: Response = client.get(self.endpoint)
        assert response.status_code == 401

    def test_permission_authorized_failed(self, client: APIClient):
        Customer.objects.create_user(email="test1", password="jfmnf123")
        tokens: Response = client.post(
            "/api/auth/login/", dict(email="test1", password="jfmnf123")
        )
        assert Customer.objects.count() == 1
        assert tokens.data["access"] is not None
        assert len(tokens.data) == 2
        client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens.data["access"])
        response: Response = client.get(self.endpoint)
        assert response.status_code == 403

    def test_admin_user_list(self, client: APIClient, admin_tokens: Response):
        baker.make(Customer, _quantity=3)
        assert admin_tokens.data["access"] is not None
        assert len(admin_tokens.data) == 2
        client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_tokens.data["access"])
        response: Response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_admin_user_create(self, admin_client: APIClient):
        response = admin_client.post(self.endpoint, self.payload)
        assert response.data["email"] == self.payload["email"]
        assert response.data["phone"] == self.payload["phone"]
        assert response.status_code == 201

    def test_admin_user_partial_update(self, admin_client: APIClient):
        user: Customer = baker.make(Customer)
        response = admin_client.patch(f"{self.endpoint}{user.id}/", self.payload)
        assert response.status_code == 200
        assert response.data['email'] == self.payload["email"]
        assert response.data["phone"] == self.payload["phone"]

    def test_admin_user_update(self, admin_client: APIClient):
        response = admin_client.post(self.endpoint, self.payload)
        assert response.status_code == 201

        user_id = response.data["id"]
        prev_email = response.data["email"]
        self.payload["email"] = "test_updated@gmail.com"
        response = admin_client.put(f"{self.endpoint}{user_id}/", self.payload)

        assert response.status_code == 200
        assert response.data["email"] != prev_email

    def test_admin_user_delete(self, admin_client: APIClient):
        response = admin_client.post(self.endpoint, self.payload)
        user_id = response.data["id"]
        assert response.status_code == 201
        response = admin_client.delete(f"{self.endpoint}{user_id}/")
        assert response.status_code == 204
        assert Customer.objects.count() == 1


class TestAdminProductsViewset:
    endpoint = "/api/admin/products/"

    def test_admin_products_list(self, admin_client: APIClient, user: Customer, category_set: List[Category]):
        size_set = baker.make(Size, _quantity=5)
        color_set = baker.make(Color, _quantity=4)
        shop = ShopFactory.create(
            name="Testing Shop",
            user=user,
            email="testing@me.com",
            address="testingaddresss",
            verified=False,
            phone="01020304",
        )
        brand_type = BrandTypeFactory.create(
            name="BrandType"
        )
        brand = BrandFactory.create(
            name="testBrand",
            type=brand_type,
            featured=True,
        )
        product = ProductFactory.create(
            title="testProd",
            brand=brand,
            shop=shop,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=InMemoryUploadedFile(
                file=StringIO("test"),
                field_name="test",
                name="test.jpg",
                content_type="image/jpeg",
                size=1,
                charset="utf-8",
            ),

        )

        print(shop)
        print(brand_type)
        print(brand)
        response = admin_client.get(self.endpoint)
        assert response.status_code == 200

    def test_admin_products_create(self, admin_client: APIClient):
        pass
