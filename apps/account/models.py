from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    CLIENT = "client"
    COMPANY = "company"

    USER_TYPE = (
        (CLIENT, "client"),
        (COMPANY, "company")
    )
    phone_number = models.CharField(max_length=13)
    verification_code = models.IntegerField(blank=True, null=True)
    verification_code_created_at = models.DateTimeField(blank=True, null=True)
    hourly_cost = models.PositiveIntegerField(blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default=CLIENT)
    image = models.ImageField(blank=True, null=True, upload_to="account_image/")
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    registered = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name if self.first_name else self.phone_number


class ChangedPhone(models.Model):
    user = models.OneToOneField(CustomUser, related_name="changed_phone", on_delete=models.CASCADE)
    number = models.CharField(max_length=15, blank=True, null=True)
    verification_code = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)


class Location(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_location")
    address = models.CharField(max_length=255, blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)




