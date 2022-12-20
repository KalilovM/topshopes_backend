from django.db import models


class Page(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, db_index=True)
    content = models.JSONField(db_index=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="post_images", blank=True, null=True, db_index=True
    )

    def __str__(self):
        return self.title


class PageNavigation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    page = models.ForeignKey("pages.Page", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PageNavigationCategory(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    page_navigation = models.ForeignKey(
        "pages.PageNavigation", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
