from django.contrib import admin
from .models import Product, Category, ProductVariant, Image, Review, Brand, BrandType


for model in [Product, Category, ProductVariant, Image, Review, Brand, BrandType]:
    admin.site.register(model)
