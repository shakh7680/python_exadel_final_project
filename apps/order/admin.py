from django.contrib import admin
from apps.order import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']