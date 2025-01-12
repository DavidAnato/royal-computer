from django.contrib import admin
from django.utils.html import format_html
from .models import *

   

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1
    fields = ('image',)  # Ne pas inclure `image_thumbnail` ici
    readonly_fields = ('image_thumbnail',)  # Ajoutez-le ici pour l'affichage uniquement

    def image_thumbnail(self, obj):
        if obj.image:
            # Vérifiez si l'URL est une image ou une vidéo
            if obj.image.url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html(
                    '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                    obj.image.url
                )
            else:
                return format_html(
                    '<video src="{}" style="max-width: 100px; max-height: 100px;" controls></video>',
                    obj.image.url
                )
        return "No image/video"

    image_thumbnail.short_description = 'Preview'

class KeyWordInline(admin.TabularInline):
    model = KeyWord
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'promo_price', 'in_promo', 'in_stock', 'is_new', 'is_vedette')
    list_filter = ('category', 'brand', 'in_promo', 'in_stock', 'is_new')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'category', 'brand', 'description')
        }),
        ('Images', {
            'fields': (('image_tag', 'image', 'image_secondary_tag', 'image_secondary'),),
        }),
        ('Prix et disponibilité', {
            'fields': ('price', 'promo_price', 'in_promo', 'in_stock')
        }),
        ('Options', {
            'fields': ('is_new', 'is_vedette')
        }),
        ('Autre', {
            'fields': ('specification', 'warranty_info', 'display', 'processor_capacity', 'camera_quality', 'memory', 'harddisk_capacity', 'graphics')
        }),
    )

    inlines = [KeyWordInline, AdditionalImageInline]

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    def image_secondary_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image_secondary.url))

    image_tag.short_description = 'Image'
    image_secondary_tag.short_description = 'Image secondaire'

    readonly_fields = ('image_tag', 'image_secondary_tag')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating')
    list_filter = ('product', 'rating')
    search_fields = ('user__username', 'product__name')
    list_editable = ('rating',)

class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_thumbnail')

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    image_thumbnail.short_description = 'Image'

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(KeyWord)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
