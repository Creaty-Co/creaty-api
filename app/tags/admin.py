from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from app.mentors.models import Mentor
from app.tags.models import Category, CategoryTag, Tag


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'shortcut': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


class TagInline(admin.TabularInline):
    verbose_name = "Tags"
    model = CategoryTag
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['title', 'shortcut', 'link']
    readonly_fields = ['link', 'display_icon', 'mentors']
    fieldsets = [
        (None, {'fields': ['display_icon', 'icon', 'title', 'shortcut', 'link']}),
        ('Mentors', {'fields': ['mentors']}),
    ]
    inlines = [TagInline]

    def link(self, obj):
        url = f"https://{settings.WEB_DOMAIN}/mentors/{obj.shortcut}"
        return format_html('<a href="{}">{}</a>', url, url)

    def display_icon(self, obj):
        return format_html('<img src="{}" width="100"/>', obj.icon.url)

    def mentors(self, obj):
        mentors = Mentor.objects.filter(tags__categories=obj).distinct()
        if mentors.exists():
            return '\n'.join([f"🔹 {mentor}" for mentor in mentors])
        return "No mentors"


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'shortcut': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


class CategoryInline(admin.TabularInline):
    verbose_name = "Categories"
    model = CategoryTag
    extra = 1


class MentorInline(admin.TabularInline):
    verbose_name = "Mentors"
    model = Mentor.tags.through
    extra = 1


class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ['title', 'shortcut', 'link']
    fields = ['title', 'shortcut', 'link']
    readonly_fields = ['link']
    inlines = [CategoryInline, MentorInline]

    def link(self, obj):
        url = f"https://{settings.WEB_DOMAIN}/mentors/{obj.shortcut}"
        return format_html('<a href="{}">{}</a>', url, url)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
