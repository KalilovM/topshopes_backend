from django.db import models
import uuid
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey

# TODO: barcode for product and qr code
class Link(models.Model):
    facebook = models.CharField(max_length=255, unique=True)
    youtube = models.CharField(max_length=255, unique=True)
    twitter = models.CharField(max_length=255, unique=True)
    instagram = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["id"]


class Shop(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Shop's id"
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="Shop's name")
    slug = AutoSlugField(
        populate_from="name", unique=True, db_index=True, verbose_name="Link to shop"
    )
    user = models.ForeignKey(
        "users.Customer",
        on_delete=models.CASCADE,
        related_name="shop",
        verbose_name="User",
    )
    email = models.CharField(max_length=100, unique=True, verbose_name="Shop's email")
    address = models.CharField(max_length=200, verbose_name="Shop's address")
    verified = models.BooleanField(default=False, verbose_name="Is shop verified?")
    coverPicture = models.ImageField(
        upload_to="shop/covers/", verbose_name="Shop's cover picture"
    )
    profilePicture = models.ImageField(
        upload_to="shop/profiles/", verbose_name="Shop's profile picture"
    )
    socialLinks = models.ForeignKey(
        Link, on_delete=models.SET_NULL, null=True, verbose_name="Shop's social links"
    )

    class Meta:
        ordering = ["name"]


class Size(models.Model):
    name = models.CharField(max_length=15, verbose_name="Product's size")


class Color(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name="Color's name")
    color = models.CharField(max_length=20, unique=True, verbose_name="Color")


class BrandType(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Image(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="image"
    )
    # TODO: create helper function to rename and return path of image
    image = models.ImageField(upload_to="products/gallery/")


class Category(MPTTModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    icon = models.ImageField(upload_to="category/icons/", null=True, blank=True)
    image = models.ImageField(upload_to="category/images/")
    name = models.CharField(max_length=50, verbose_name="Category name")
    slug = AutoSlugField(populate_from="name")
    description = models.TextField()
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    featured = models.BooleanField(default=False)

    class Meta:
        order_insertion_by = ["name"]


class Brand(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Brand's id"
    )
    name = models.CharField(max_length=100, verbose_name="Brand's name", unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name="Brand's link")
    image = models.ImageField(upload_to="brands/", verbose_name="Brand's image")
    type = models.ForeignKey(
        BrandType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Type of the Brand",
    )
    featured = models.BooleanField(default=False, verbose_name="Is featured?")

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name="Product's id"
    )
    title = models.CharField(max_length=150, verbose_name="Product's title")
    slug = AutoSlugField(
        populate_from="title", unique=True, verbose_name="Link to product"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, verbose_name="Product's brand"
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name="Product's shop",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Product's price"
    )
    size = models.ManyToManyField(
        Size, related_name="size", verbose_name="Product's sizes"
    )
    colors = models.ManyToManyField(
        Color, related_name="color", verbose_name="Product's colors"
    )
    discount = models.IntegerField(default=0, verbose_name="Product's discount")
    thumbnail = models.ImageField(
        upload_to="products/thumbnail/", verbose_name="Product's thumbnail"
    )
    category = models.ManyToManyField(
        Category, related_name="category", verbose_name="Product's category"
    )


class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rating = models.IntegerField(default=5)
    published = models.BooleanField(default=False)
    # TODO: check about how to validate textfields
    comment = models.TextField()
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ["rating"]
