from django.db import models

from core.helpers import PathAndRename


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.JSONField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to=PathAndRename("posts_images/"), blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_posted"]
