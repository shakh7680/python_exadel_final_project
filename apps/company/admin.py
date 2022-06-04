from django.contrib import admin
from apps.company import models


@admin.register(models.CompanyServiceEquipments)
class CompanyServiceEquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'company']
    list_display_links = ['id', 'company']


@admin.register(models.CompanyServiceEquipmentImages)
class CompanyServiceEquipmentImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment']
    list_display_links = ['id', 'equipment']


@admin.register(models.Rating)
class CompanyRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'star']
    list_display_links = ['id', 'company']


@admin.register(models.CompanyContacts)
class CompanyContactsAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'phone_number']
    list_display_links = ['id', 'company']
