from django.contrib import admin
from .models import (
    Product,
    Category,
    ProductVariant,
    Image,
    Brand,
    BrandType,
    ProductAttribute,
    ProductAttributeValue,
)


for model in [Product, Category, ProductVariant, Image, Brand, BrandType, ProductAttribute, ProductAttributeValue]:
    admin.site.register(model)
