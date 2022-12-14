from model_bakery import baker
from pprint import pprint
import factory
import json
import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from shops.models import Brand, BrandType, Category, Product, Shop
from users.models import Customer

pytestmark = pytest.mark.django_db


class TestAdminUserEndpoints:
    """
    Test /api/admin/users/
    """

    # TODO: About admin creation

    endpoint = "/api/admin/users/"

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
        print(tokens.data)
        assert len(tokens.data) == 2
        client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens.data["access"])
        response: Response = client.get(self.endpoint)
        assert response.status_code == 403

    def test_user_admin_user_list(self, client: APIClient):
        Customer.objects.create_superuser("admin", "admin")

        baker.make(Customer, _quantity=3)

        admin_data = dict(email="admin", password="admin")

        tokens_data: Response = client.post("/api/auth/login/", admin_data)
        assert tokens_data.data["access"] is not None
        assert len(tokens_data.data) == 2
        client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens_data.data["access"])
        response: Response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4
