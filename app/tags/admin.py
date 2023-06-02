from django import forms
from django.contrib import admin
from django.db import models

from .models import Category, CategoryTag, Tag


class CategoryTagInline(admin.TabularInline):
    model = CategoryTag
    extra = 1
    verbose_name = "Tag"
    verbose_name_plural = "Tags"


class TagCategoryInline(admin.TabularInline):
    model = CategoryTag
    extra = 1
    verbose_name = "Category"
    verbose_name_plural = "Categories"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTagInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput(attrs={'size': '20'})}
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TagCategoryInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput(attrs={'size': '20'})},
    }
