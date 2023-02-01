from django.contrib import admin

from .models import Payment, TransferMoney

admin.site.register(Payment)
admin.site.register(TransferMoney)
