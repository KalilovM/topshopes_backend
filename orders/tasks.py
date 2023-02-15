from .models import Order
from payments.models import TransferMoney
from datetime import timedelta
from django.utils import timezone


def check_payment_status(order):
    order.save()
