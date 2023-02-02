from django.contrib import admin

from app.tags.models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'shortcut')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'shortcut')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
