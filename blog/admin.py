from django.contrib import admin
from django.utils.html import format_html

from .models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author__username', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_image', 'published_date')
    list_filter = ('published_date', 'categories', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    def display_image(self, obj):
        return format_html('<img src="{}" width="60px" height="auto" />'.format(obj.image.url))
    display_image.short_description = 'Image'

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
