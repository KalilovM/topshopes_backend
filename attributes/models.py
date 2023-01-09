from django.db import models


class Attribute(models.Model):
    """
    Product attribute model
    """

    name = models.CharField(max_length=100, verbose_name="Attribute name")
    category = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, related_name="attributes"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Product attribute"
        verbose_name_plural = "Product attributes"


class AttributeValue(models.Model):
    """
    Product attribute value model
    """

    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="attribute_values",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
    )
    value = models.CharField(max_length=100, verbose_name="Attribute value")

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ["value"]
        verbose_name = "Product attribute value"
        verbose_name_plural = "Product attribute values"
