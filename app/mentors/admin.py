from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Mentor, Package


class PackageInline(admin.TabularInline):
    model = Package
    extra = 1


class MentorAdminForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'
        widgets = {
            'slug': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'company': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'first_name': forms.TextInput(
                attrs={'style': 'height: 15px; width: 200px'}
            ),
            'last_name': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    form = MentorAdminForm
    list_display = ['__str__', 'is_draft']
    list_display_links = ['__str__']
    fields = [
        'is_draft',
        'slug',
        'display_avatar',
        'avatar',
        'resume',
        'first_name',
        'last_name',
        'country',
        'city',
        'tags',
        'experience',
        'what_help',
        'price',
        'trial_meeting',
    ]
    filter_horizontal = ['tags']
    readonly_fields = ['display_avatar']
    search_fields = ['first_name', 'last_name']
    inlines = [PackageInline]

    def display_avatar(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)

    display_avatar.short_description = 'Avatar image'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
