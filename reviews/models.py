from django.db import models
import uuid


class Review(models.Model):
    """
    Rating model for product
    """

    RATINGS = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.Customer", on_delete=models.CASCADE, related_name="reviews"
    )
    product_variant = models.ForeignKey(
        "products.ProductVariant", on_delete=models.CASCADE, related_name="reviews"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="reviews"
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # update product rating
        product = self.product
        product_rating = product.reviews.aggregate(models.Avg("rating"))["rating__avg"]
        product.rating = product_rating
        product.save()
