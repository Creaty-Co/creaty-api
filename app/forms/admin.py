from django import forms
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from app.forms.models import Application
from app.forms.models.choices import FormType
from app.users.models import User


class UserRegisteredFilter(admin.SimpleListFilter):
    title = "User registered"
    parameter_name = 'user_registered'

    def lookups(self, request, model_admin):
        return (('yes', "Yes"), ('no', "No"))

    def queryset(self, request, queryset):
        match self.value():
            case 'yes':
                return queryset.filter(
                    email__in=User.objects.all().values_list('email', flat=True)
                )
            case 'no':
                return queryset.exclude(
                    email__in=User.objects.all().values_list('email', flat=True)
                )
        return queryset


class UserVerifiedFilter(admin.SimpleListFilter):
    title = "User verified"
    parameter_name = 'user_verified'

    def lookups(self, request, model_admin):
        return (('yes', "Yes"), ('no', "No"))

    def queryset(self, request, queryset):
        is_verified = (
            True if self.value() == 'yes' else False if self.value() == 'no' else None
        )
        if is_verified is None:
            return queryset
        return queryset.filter(
            email__in=User.objects.filter(is_verified=is_verified).values_list(
                'email', flat=True
            )
        )


class CreatedAtFilter(admin.SimpleListFilter):
    title = "Created at"
    parameter_name = 'last_24_hours'

    def lookups(self, request, model_admin):
        return (('last_24_hours', "Last 24 hours"),)

    def queryset(self, request, queryset):
        if self.value() == 'last_24_hours':
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            return queryset.filter(created_at__gte=last_24_hours)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'form_type',
        'name',
        'email',
        'URL',
    ]
    list_filter = [
        'form__type',
        CreatedAtFilter,
        UserRegisteredFilter,
        UserVerifiedFilter,
    ]
    ordering = ['-created_at']
    formfield_overrides = {
        models.TextField: {
            'widget': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'})
        }
    }

    def get_fields(self, request, obj=None):
        if request.user.has_perm('forms.change_application'):
            return super().get_fields(request, obj)
        return [
            'form_type',
            'URL',
            'name',
            'email',
            'about',
            'link',
            'created_at',
        ]

    def URL(self, obj):
        return format_html('<a href="{}">{}</a>', obj.url, obj.url)

    def form_type(self, obj):
        return FormType(obj.form.type).label
