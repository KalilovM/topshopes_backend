import uuid
from decimal import Decimal

from autoslug import AutoSlugField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.helpers import PathAndRename
from shops.models import Shop


class Color(models.Model):
    """
    Product color model
    """

    name = models.CharField(max_length=15, unique=True, verbose_name="Color's name")
    color = models.CharField(max_length=20, unique=True, verbose_name="Color")

    def __str__(self):
        return self.name


class BrandType(models.Model):
    """
    Brand types
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    """
    Product image model
    """

    product_variant = models.ForeignKey(
        "ProductVariant", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=PathAndRename("products/gallery/"))

    def __str__(self):
        return f"{self.pk} {self.product_variant}"


class Category(MPTTModel):
    """
    Category model for product
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    icon = models.ImageField(
        upload_to=PathAndRename("category/icons/"), null=True, blank=True
    )
    image = models.ImageField(upload_to=PathAndRename("category/images/"))
    name = models.CharField(max_length=50, verbose_name="Category name", unique=True)
    slug = AutoSlugField(populate_from="name", editable=False)
    description = models.TextField()
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    featured = models.BooleanField(default=False)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} {self.name} subcategory"
        return f"{self.name} category"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ["name"]


class Size(models.Model):
    """
    Product size model
    """

    name = models.CharField(max_length=15, verbose_name="Product's size", unique=True)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Brand for product
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Brand's id"
    )
    name = models.CharField(max_length=100, verbose_name="Brand's name", unique=True)
    slug = AutoSlugField(
        populate_from="name", unique=True, verbose_name="Brand's link", editable=False
    )
    image = models.ImageField(
        upload_to=PathAndRename("brands/"), verbose_name="Brand's image"
    )
    type = models.ForeignKey(
        BrandType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Type of the Brand",
    )
    featured = models.BooleanField(default=False, verbose_name="Is featured?")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ProductVariant(models.Model):
    """
    Color, size and thumbnail variants of product
    """

    STATUSES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("coming_soon", "Coming soon"),
    )

    color = models.ForeignKey(
        "products.Color", on_delete=models.PROTECT, related_name="variant"
    )

    size = models.ForeignKey(
        "products.Size", on_delete=models.PROTECT, related_name="size"
    )

    thumbnail = models.ImageField(
        upload_to=PathAndRename("products/thumbnail/"),
        verbose_name="Product's thumbnail",
    )
    stock = models.PositiveSmallIntegerField(default=0)
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="variants"
    )
    status = models.CharField(choices=STATUSES, max_length=20, default="available")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Product's price"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Product's discounted price",
        editable=False,
    )
    discount = models.PositiveSmallIntegerField(
        default=0, verbose_name="Product's discount"
    )

    def change_status(self):
        if self.stock == 0:
            self.status = "unavailable"

    def sell(self):
        if self.stock >= 0:
            self.stock -= 1

    def get_discount_price(self):
        self.discount_price = self.price - (self.price * self.discount_price / 100)

    def save(self, *args, **kwargs):
        self.change_status()
        self.get_discount_price()
        super(ProductVariant, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} {self.color} {self.size}"


class Product(models.Model):
    """
    Product for shop model
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Product's id"
    )
    title = models.CharField(max_length=150, verbose_name="Product's title")
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        verbose_name="Link to product",
        editable=False,
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, verbose_name="Product's brand"
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Product's shop",
    )
    rating = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)
    unit = models.CharField(max_length=50)
    published = models.BooleanField(default=True)

    # def get_rating(self):
    #     self.objects.reviews.
    #

    def __str__(self):
        return f"{self.shop.name} {self.title}"


class Review(models.Model):
    """
    Review for product
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rating = models.IntegerField(default=5)
    published = models.BooleanField(default=False)
    comment = models.TextField()
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return f"{self.customer.email} {self.product.title}"

    class Meta:
        ordering = ["rating"]