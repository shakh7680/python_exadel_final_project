from django.contrib import admin
from apps.client.models import SavedCompany


@admin.register(SavedCompany)
class SavedCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'company']
    list_display_links = ['id', 'client']