from django.db import models
from django.utils.text import slugify


class Slider(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Slider, self).save(*args, **kwargs)


class Slide(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    content = models.JSONField(db_index=True)
    link = models.CharField(max_length=100, db_index=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="post_images", blank=True, null=True, db_index=True
    )
    slider = models.ForeignKey(
        "sliders.Slider", on_delete=models.CASCADE, db_index=True, related_name="slides"
    )

    def __str__(self):
        return self.title
