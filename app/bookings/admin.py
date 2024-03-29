from django.contrib import admin
from django.forms import TextInput
from django.utils import timezone
from django.utils.html import format_html

from ..users.models import User
from .models import AbstractBooking, HourlyBooking, PackageBooking, TrialBooking


class CreatedAtFilter(admin.SimpleListFilter):
    title = "Created at"
    parameter_name = 'last_24_hours'

    def lookups(self, request, model_admin):
        return (('last_24_hours', "Last 24 hours"),)

    def queryset(self, request, queryset):
        if self.value() == 'last_24_hours':
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            return queryset.filter(created_at__gte=last_24_hours)


class _BaseBookingAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_filter = ['mentor', CreatedAtFilter]
    readonly_fields = ['mentor_url', 'has_discount']

    def mentor_url(self, obj: AbstractBooking):
        mentor = obj.mentor
        return format_html('<a href="{}">{}</a>', mentor.url, mentor.url)

    def has_discount(self, obj: AbstractBooking):
        try:
            return User.objects.get(email=obj.email).has_discount
        except User.DoesNotExist:
            return False

    has_discount.boolean = True

    def _get_price(self, obj: AbstractBooking):
        return obj.price

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            formfield.widget = TextInput(
                attrs=formfield.widget.attrs | {'style': 'height: 15px; width: 200px'}
            )
        return formfield


@admin.register(TrialBooking)
class TrialBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor_url']


@admin.register(HourlyBooking)
class HourlyBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor_url']
    readonly_fields = _BaseBookingAdmin.readonly_fields + ['price']

    def price(self, obj: AbstractBooking):
        return self._get_price(obj)


@admin.register(PackageBooking)
class PackageBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor_url', 'package']
    readonly_fields = _BaseBookingAdmin.readonly_fields + ['discounted_price']

    def discounted_price(self, obj: AbstractBooking):
        return self._get_price(obj)
