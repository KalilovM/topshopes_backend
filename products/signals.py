from django.db.models.signals import pre_save
from .models import Product
from django.dispatch import receiver


@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, **kwargs):
    print(sender, instance)
    print(**kwargs)
