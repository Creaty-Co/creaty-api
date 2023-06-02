from django.contrib import admin

from .models import Category, CategoryTag, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    pass
