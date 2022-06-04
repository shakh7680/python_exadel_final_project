from django.db import models
from apps.account.models import CustomUser


class Order(models.Model):
    ACCEPTED = ""
    REQUESTED = ""
    IN_PROGRESS = ""
    COMPLETED = ""
    CANCELLED = ""
    ORDER_STATUS_LIST = [REQUESTED, ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED]
    STATUS = (
        (REQUESTED, "requested"),
        (ACCEPTED, "accepted"),
        (IN_PROGRESS, "in_progress"),
        (COMPLETED, "completed"),
        (CANCELLED, "cancelled")
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    company = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="doer_company",
                                blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.FloatField(blank=True, null=True)
    urgent = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default=REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
