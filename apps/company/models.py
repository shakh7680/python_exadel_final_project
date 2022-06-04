from django.db import models
from apps.account.models import CustomUser


class CompanyServiceEquipments(models.Model):
    company = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='company_equipments')
    equipment_model = models.CharField(max_length=255)
    additional_info = models.CharField(max_length=255, blank=True, null=True)


class CompanyServiceEquipmentImages(models.Model):
    equipment = models.ForeignKey(CompanyServiceEquipments, on_delete=models.CASCADE, related_name='equipment_images')
    image = models.ImageField(upload_to="equipment-images/")


class Rating(models.Model):
    RATING = (
        (0, 0),
        (0.5, 0.5),
        (1, 1),
        (1.5, 1.5),
        (2, 2),
        (2.5, 2.5),
        (3, 3),
        (3.5, 3.5),
        (4, 4),
        (4.5, 4.5),
        (5, 5),
        (5, 5),
    )

    company = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='company_rating')
    appraiser = models.ForeignKey('account.CustomUser', on_delete=models.SET_NULL, blank=True, null=True)
    star = models.FloatField(choices=RATING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    # Only company can be rated
    def clean(self):
        company = CustomUser.objects.get(id=self.company.id)
        if company.role != 'company':
            msg = "You should choose company for rating"
            self.add_error('error', msg)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class CompanyContacts(models.Model):
    company = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='company_contacts')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)
    skype = models.CharField(max_length=50, blank=True, null=True)