from django.contrib import admin
from django.forms import TextInput
from django.utils.html import format_html

from .models import HourlyBooking, PackageBooking, TrialBooking


class _BaseBookingAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_filter = ['mentor']
    readonly_fields = ['mentor_url']

    def mentor_url(self, obj):
        mentor = obj.mentor
        return format_html('<a href="{}">{}</a>', mentor.url, mentor.url)

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
    readonly_fields = ['price']

    def price(self, obj):
        return obj.mentor.price


@admin.register(PackageBooking)
class PackageBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor_url', 'package']
    readonly_fields = ['discounted_price']

    def discounted_price(self, obj):
        return obj.mentor.price * (1 - obj.package.discount / 100)
