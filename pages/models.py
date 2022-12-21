from django.db import models


class PageCategory(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)

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
        "pages.PageCategory", on_delete=models.CASCADE, db_index=True, related_name="pages"
    )

    def __str__(self):
        return self.title
