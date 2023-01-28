import uuid
from django.utils.text import slugify

from django.db import models

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
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="Shop's slug", editable=False
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
