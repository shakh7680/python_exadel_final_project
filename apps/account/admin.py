from django.contrib import admin
from django.utils.text import gettext_lazy as _

from .models import CustomUser, ChangedPhone, Location


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main'), {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone_number', "verification_code", 'user_type',
                     'hourly_cost', 'image', 'is_active', 'verification_code_created_at',
                     'registered')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'phone_number', 'first_name', 'last_name', 'created_at'),
        }),
    )

    list_display = ['id', 'phone_number', 'first_name', 'user_type']
    list_display_links = ['phone_number', 'first_name']
    list_filter = ("user_type", )


admin.site.register(ChangedPhone)
admin.site.register(Location)