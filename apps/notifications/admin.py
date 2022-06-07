from django.contrib import admin
from apps.notifications import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']