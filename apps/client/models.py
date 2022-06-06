from django.db import models
from ..account import models as account_models
from django.core.exceptions import ValidationError


class SavedCompany(models.Model):
    client = models.ForeignKey(account_models.CustomUser, on_delete=models.CASCADE, related_name="saved_company")
    company = models.ForeignKey(account_models.CustomUser, on_delete=models.CASCADE, related_name="saved_by_client")