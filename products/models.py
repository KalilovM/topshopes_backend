import uuid
from django.utils.text import slugify
from decimal import Decimal

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.helpers import PathAndRename
from shops.models import Shop


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
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    featured = models.BooleanField(default=False)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} {self.name} subcategory"
        return f"{self.name} category"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ["name"]


class Brand(models.Model):
    """
    Brand for product
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Brand's id"
    )
    name = models.CharField(max_length=100, verbose_name="Brand's name", unique=True)
    slug = models.SlugField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]


class ProductAttribute(models.Model):
    """
    Product attribute model
    """

    name = models.CharField(max_length=100, verbose_name="Attribute name")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="attributes"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Product attribute"
        verbose_name_plural = "Product attributes"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product name")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    unit = models.CharField(max_length=100, verbose_name="Product unit")
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=Decimal(0.0),
        verbose_name="Product rating",
    )
    featured = models.BooleanField(default=False, verbose_name="Is featured?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.shop.name + "-" + self.name
        self.slug = slugify(slug)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductVariant(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Product variant price"
    )
    discount = models.IntegerField(
        verbose_name="Product variant discount", null=True, blank=True
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Product variant discount price",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    stock = models.IntegerField(verbose_name="Product variant quantity")
    thumbnail = models.ImageField(
        upload_to=PathAndRename("products/thumbnails/"),
        verbose_name="Product variant thumbnail",
    )

    def __str__(self):
        return f"{self.attribute_values.first().value} - {self.attribute_values.last().value}"

    def save(self, *args, **kwargs):
        # calculate discount price with category tax
        self.price = self.price + (self.price * self.product.category.tax / 100)
        if self.discount:
            self.discount_price = self.price - (self.price * self.discount / 100)
        else:
            self.discount_price = None

        if self.stock == 0:
            self.status = "unavailable"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["product"]
        verbose_name = "Product variant"
        verbose_name_plural = "Product variants"


class ProductAttributeValue(models.Model):
    """
    Product attribute value model
    """

    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="attribute_values"
    )
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="values",
    )
    value = models.CharField(max_length=100, verbose_name="Attribute value")

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ["value"]
        verbose_name = "Product attribute value"
        verbose_name_plural = "Product attribute values"
