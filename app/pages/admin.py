from django.contrib import admin

from .models import Page, PageMentors


class PageMentorsInline(admin.TabularInline):
    model = PageMentors
    extra = 1
    ordering = ['index']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [PageMentorsInline]
    list_display = ['__str__']
    list_filter = [
        'tag',
        'category',
    ]
    search_fields = [
        'tag__name',
        'category__name',
    ]
    filter_horizontal = ['tags']
