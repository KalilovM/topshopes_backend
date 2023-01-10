from django.contrib import admin

from .models import Attribute, AttributeValue

admin.site.register(Attribute)
admin.site.register(Attribute, AttributeValue)
