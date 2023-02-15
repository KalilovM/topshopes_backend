from .models import Order
from payments.models import TransferMoney
from datetime import timedelta
from django.utils import timezone


def check_payment_status(order):
    order.save()
    tax = order.product_variant.tax_price * order.quantity
    TransferMoney.objects.create(payment = order.payment, shop = order.shop, amount=order.total_price, tax=tax)