from django import forms
from django.conf import settings
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
            'city': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['what_help'].label = "How can I help"


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    form = MentorAdminForm
    list_display = ['__str__', 'url', 'is_draft']
    list_display_links = ['__str__']
    list_editable = ['is_draft']
    list_filter = ['is_draft']

    fieldsets = (
        (
            "Profile Information",
            {
                'fields': (
                    'is_draft',
                    'slug',
                    'link',
                    'display_avatar',
                    'avatar',
                    'first_name',
                    'last_name',
                    'email',
                    'country',
                    'city',
                )
            },
        ),
        (
            "Professional Details",
            {
                'fields': (
                    'languages',
                    'tags',
                    'resume',
                    'experience',
                    'what_help',
                    'price',
                    'trial_meeting',
                )
            },
        ),
    )
    filter_horizontal = ['tags', 'languages']
    readonly_fields = ['display_avatar', 'url']
    search_fields = ['first_name', 'last_name']
    inlines = [PackageInline]

    def display_avatar(self, obj):
        return format_html('<img src="{}" width="500"/>', obj.avatar.url)

    display_avatar.short_description = 'Avatar image'

    def url(self, obj):
        url = f"https://{settings.WEB_DOMAIN}/user/{obj.slug}"
        return format_html('<a href="{}">{}</a>', url, url)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


