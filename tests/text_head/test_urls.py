from model_bakery import baker
import factory
import json
import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from shops.models import Brand, BrandType, Category, Product, Shop
from users.models import Customer

pytestmark = pytest.mark.django_db


class TestAdminUserEndpoints:

    endpoint = "/api/admin/users/"

    def test_list(self, client: APIClient):
        baker.make(Customer, _quantity=3)

        response: Response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3
