from django.db import models
from autoslug import AutoSlugField


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
