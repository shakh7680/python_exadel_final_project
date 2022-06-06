from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.account.models import CustomUser, Location
from django.core.exceptions import ValidationError


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
        if company.user_type != 'company':
            raise ValidationError("You should choose company for rating!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_user_cashilok(sender, instance, created, **kwargs):
    if created:
        if instance.user_type in CustomUser.COMPANY:
            CompanyContacts.objects.create(company=instance)
            Location.objects.create(user=instance)
        else:
            pass


class CompanyContacts(models.Model):
    company = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE, related_name='company_contacts')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)
    skype = models.CharField(max_length=50, blank=True, null=True)