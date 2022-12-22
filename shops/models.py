import uuid

from autoslug import AutoSlugField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.helpers import PathAndRename


# TODO: barcode for product and qr code


class Shop(models.Model):
    """
    Simple shop model
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Shop's id"
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="Shop's name")
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        db_index=True,
        verbose_name="Link to shop",
        editable=False,
    )
    user = models.OneToOneField(
        "users.Customer",
        on_delete=models.CASCADE,
        related_name="shop",
        verbose_name="User",
    )
    email = models.CharField(max_length=100, unique=True, verbose_name="Shop's email")
    address = models.CharField(max_length=200, verbose_name="Shop's address")
    verified = models.BooleanField(default=False, verbose_name="Is shop verified?")
    phone = models.CharField(max_length=100, unique=True)
    cover_picture = models.ImageField(
        upload_to=PathAndRename("shop/covers/"), verbose_name="Shop's cover picture"
    )
    profile_picture = models.ImageField(
        upload_to=PathAndRename("shop/profiles/"), verbose_name="Shop's profile picture"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Link(models.Model):
    """
    Shops links
    One link - one social network
    """

    name = models.CharField(max_length=30, verbose_name="Social Network")
    link = models.CharField(max_length=255, verbose_name="Social Network Link")
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="links",
        related_query_name="links",
        verbose_name="Link to shop",
    )

    def __str__(self):
        return f"Links {self.id}"

    class Meta:
        ordering = ["id"]


class Size(models.Model):
    """
    Product size model
    """

    name = models.CharField(max_length=15, verbose_name="Product's size", unique=True)

    def __str__(self):
        return self.name


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

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=PathAndRename("products/gallery/"))

    def __str__(self):
        return f"{self.pk} {self.product}"


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


class Product(models.Model):
    """
    Product for shop model
    """

    STATUSES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("coming_soon", "Coming soon"),
    )

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
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Product's price"
    )
    sizes = models.ManyToManyField(
        Size,
        related_name="sizes",
        verbose_name="Product's sizes",
    )
    status = models.CharField(choices=STATUSES, max_length=20, default="available")
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=50)
    published = models.BooleanField(default=True)
    colors = models.ManyToManyField(
        Color, verbose_name="Product's colors", related_name="colors"
    )
    discount = models.IntegerField(default=0, verbose_name="Product's discount")
    thumbnail = models.ImageField(
        upload_to=PathAndRename("products/thumbnail/"),
        verbose_name="Product's thumbnail",
    )
    categories = models.ManyToManyField(
        Category, related_name="category", verbose_name="Product's category"
    )

    def __str__(self):
        return f"{self.shop.name} {self.title}"


class Review(models.Model):
    """
    Review for product
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rating = models.IntegerField(default=5)
    published = models.BooleanField(default=False)
    # TODO: check about how to validate textfields
    comment = models.TextField()
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.username} {self.product.title}"

    class Meta:
        ordering = ["rating"]
