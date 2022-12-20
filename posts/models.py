from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.JSONField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    author = models.ForeignKey("users.Customer", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_posted"]
