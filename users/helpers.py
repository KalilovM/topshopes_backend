from django.http import HttpRequest
from .models import Customer
from typing import Dict


class HttpRequestAutenticated(HttpRequest):
    """
    Annotate for user in HttpRequest
    """

    user: Customer
    data: Dict
