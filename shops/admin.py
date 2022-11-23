from django.contrib import admin
from .models import (
    Link,
    Shop,
    Size,
    Color,
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    Review,
)

admin.site.register(Link)
admin.site.register(Shop)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(BrandType)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Review)
