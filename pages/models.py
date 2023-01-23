from autoslug import AutoSlugField
from django.db import models

from core.helpers import PathAndRename


class PageCategory(models.Model):
    id = AutoSlugField(populate_from="title", primary_key=True)
    title = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    content = models.JSONField(db_index=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="post_images", blank=True, null=True, db_index=True
    )
    category = models.ForeignKey(
        "pages.PageCategory",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="pages",
    )

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    email = models.EmailField(null=True)
    support_email = models.EmailField(null=True)
    header_phone = models.CharField(max_length=100, null=True, blank=True)
    footer_phone = models.CharField(max_length=100, null=True, blank=True)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=155, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    gmail = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    map = models.TextField(max_length=2000, null=True, blank=True)
    logo = models.ImageField(
        upload_to=PathAndRename("site_settings/logos/"), null=True, blank=True
    )

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.__class__.objects.exists():
            super().save(*args, **kwargs)
