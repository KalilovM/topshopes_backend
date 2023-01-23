from django.db import models
import uuid
from core.helpers import PathAndRename


class Application(models.Model):
    """
    Request model
    """
    REGISTRATION_CHOICES = (
        ("with_nds", "with NDS"),
        ("without_nds", "without NDS"),
    )
    STATUSES = (
        ("moderation", "moderation"),
        ("approved", "approved"),
        ("rejected", "rejected"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    document = models.FileField(upload_to=PathAndRename("documents/"))
    INN = models.CharField(max_length=14, null=True, blank=False)
    short_name = models.CharField(max_length=30, null=True, blank=False)
    full_name = models.CharField(max_length=200, null=True, blank=False)
    registration_form = models.CharField(max_length=20, choices=REGISTRATION_CHOICES,default="with_nds", null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    owner = models.CharField(max_length=100, null=True, blank=False)
    bank_account = models.CharField(max_length=16, null=True, blank=False)
    bik = models.CharField(max_length=9, null=True, blank=False)
    shop_name = models.CharField(max_length=100, null=True, blank=False)
    status = models.CharField(max_length=20, choices=STATUSES, null=True, blank=False, default="moderation")
    customer = models.OneToOneField(
        "users.Customer",on_delete=models.CASCADE, related_name="application"
    )

    def __str__(self) -> str:
        return self.short_name


