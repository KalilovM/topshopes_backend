from celery import shared_task
from .models import Order
from payments.models import TransferMoney
from datetime import timedelta
from django.utils import timezone


@shared_task
def check_payment_status(order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'completed'
    order.save()
    tax = order.product_variant.tax_price * order.quantity
    TransferMoney.objects.create(payment = order.payment, shop = order.shop, amount=order.total_price, tax=tax)