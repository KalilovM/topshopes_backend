import json
import pprint
from typing import List

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework.response import Response
from rest_framework.test import APIClient

from shops.models import Shop
from products.models import Product, Size, Color, Brand, Category, BrandType, Image
from tests.factories import ProductFactory
from users.models import Customer

pytestmark = pytest.mark.django_db


class TestAdminUserViewset:
    """
    Test /api/admin/users/
    """

    # TODO: About admin creation

    endpoint = "/api/admin/users/"
    payload = dict(email="test@gmail.com", phone="09090909", password="jfmnf123")

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
        assert response.data["email"] == self.payload["email"]
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

    def test_admin_products_list(
        self,
        admin_client: APIClient,
        user: Customer,
        category_set: List[Category],
        size_set: List[Size],
        color_set: List[Color],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
    ):
        product = ProductFactory.create(
            title="testProd",
            brand=brand_set,
            shop=shop_set,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )

        response: Response = admin_client.get(self.endpoint, format="json")
        # pretty print created product
        # for i in response.data:
        #     pprint.pprint(i)
        assert response.status_code == 200
        assert Product.objects.count() == 1

    def test_admin_products_create(
        self,
        admin_client: APIClient,
        category_set: List[Category],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
        color_set: List[Color],
        size_set: List[Size],
    ):
        payload = dict(
            title="testProd",
            brand=brand_set.id,
            shop=shop_set.id,
            price="100.00",
            status="available",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=[i.id for i in size_set],
            colors=[i.id for i in color_set],
            categories=[i.id for i in Category.objects.all()],
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
            description="description1",
        )
        response: Response = admin_client.post(self.endpoint, payload)
        assert response.status_code == 201
        assert Product.objects.count() == 1
        # pretty print created product
        # response_json = json.loads(response.content)
        # pprint.pprint(response_json)
        for i in range(3):
            Image.objects.create(
                product=Product.objects.first(),
                image=SimpleUploadedFile(
                    name="test_image.jpg",
                    content=open("tests/test_head/testimage.webp", "rb").read(),
                    content_type="image/jpeg",
                ),
            )
        assert Image.objects.count() == 3
        assert Product.objects.first().images.count() == 3

    def test_admin_products_partial_update(
        self,
        admin_client: APIClient,
        category_set: List[Category],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
        color_set: List[Color],
        size_set: List[Size],
    ):
        product = ProductFactory.create(
            title="testProd",
            brand=brand_set,
            shop=shop_set,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        payload = dict(
            title="testProd_updated",
            brand=brand_set.id,
            shop=shop_set.id,
            price="100.00",
            status="available",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=[i.id for i in size_set],
            colors=[i.id for i in color_set],
            categories=[i.id for i in Category.objects.all()],
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        response: Response = admin_client.patch(
            f"{self.endpoint}{product.id}/", payload
        )
        assert response.status_code == 200
        assert Product.objects.count() == 1
        assert response.data["title"] == payload["title"]

    def test_admin_products_update(
        self,
        admin_client: APIClient,
        category_set: List[Category],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
        color_set: List[Color],
        size_set: List[Size],
    ):
        product = ProductFactory.create(
            title="testProd",
            brand=brand_set,
            shop=shop_set,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        payload = dict(
            title="testProd_updated",
            brand=brand_set.id,
            shop=shop_set.id,
            price="100.00",
            status="available",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=[i.id for i in size_set],
            colors=[i.id for i in color_set],
            categories=[i.id for i in Category.objects.all()],
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        response: Response = admin_client.put(f"{self.endpoint}{product.id}/", payload)
        assert response.status_code == 200
        assert Product.objects.count() == 1
        assert response.data["title"] == payload["title"]

    def test_admin_products_delete(
        self,
        admin_client: APIClient,
        category_set: List[Category],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
        color_set: List[Color],
        size_set: List[Size],
    ):
        product = ProductFactory.create(
            title="testProd",
            brand=brand_set,
            shop=shop_set,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        response: Response = admin_client.delete(f"{self.endpoint}{product.id}/")
        assert response.status_code == 204
        assert Product.objects.count() == 0

    def test_admin_products_retrieve(
        self,
        admin_client: APIClient,
        category_set: List[Category],
        shop_set: Shop,
        brand_set: Brand,
        brandtype_set: BrandType,
        color_set: List[Color],
        size_set: List[Size],
    ):
        product = ProductFactory.create(
            title="testProd",
            brand=brand_set,
            shop=shop_set,
            price="100.00",
            status="ontest",
            rating=10,  # TODO need to test also
            unit="kg",
            published=True,
            discount=10,
            sizes=size_set,
            colors=color_set,
            categories=category_set,
            thumbnail=SimpleUploadedFile(
                name="test_image.jpg",
                content=open("tests/test_head/testimage.webp", "rb").read(),
                content_type="image/jpeg",
            ),
        )
        response: Response = admin_client.get(f"{self.endpoint}{product.id}/")
        assert response.status_code == 200
        assert Product.objects.count() == 1
