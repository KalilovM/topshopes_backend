from celery import shared_task
from .models import Order
from payments.models import TransferMoney
from datetime import timedelta
from django.utils import timezone


@shared_task
def check_payment_status():
    orders = Order.objects.filter(status='delivered')
    for order in orders:
        if order.delivered_at + timedelta(days=3) < timezone.now():
            order.status = 'completed'
            order.save()
            tax = order.product_variant.price * order.quantity * order.product_variant.product.category.tax
            TransferMoney.objects.create(order=order, shop=order.shop, amount=order.total_price,
                                         tax=tax)