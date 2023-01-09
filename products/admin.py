from django.contrib import admin

from .models import Brand, BrandType, Category, Image, Product, ProductVariant

for model in [
    Product,
    Category,
    ProductVariant,
    Image,
    Brand,
    BrandType,
]:
    admin.site.register(model)
