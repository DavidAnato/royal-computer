from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import *

# Modèles associés
admin.site.register(Language)
admin.site.register(Currency)
admin.site.register(PaymentMethod)
admin.site.register(Address)

# Personnalisation de l'interface d'administration pour le modèle CustomUser
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'phone_number_confirmed', 'photo_tag', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
        ('Préférences', {'fields': ('receive_confirmation_emails', 'receive_order_updates', 'receive_promotions', 'language', 'currency', 'payment_method', 'mobile_money_number', 'paypal_email', 'profile_visibility', 'data_sharing')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def photo_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.profile_photo.url))

    photo_tag.short_description = 'Photo de profile'

    readonly_fields = ('photo_tag',)


admin.site.register(CustomUser, CustomUserAdmin)

class MyModelAdmin(admin.ModelAdmin):
    # ...
    fieldsets = [
        ("Section title", {
            "classes": ("collapse", "expanded"),
            "fields": (...),
        }),
    ]