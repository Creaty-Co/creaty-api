from django.contrib import admin
from django.forms import TextInput

from .models import HourlyBooking, PackageBooking, TrialBooking


class _BaseBookingAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_filter = ['mentor']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            formfield.widget = TextInput(
                attrs=formfield.widget.attrs | {'style': 'height: 15px; width: 200px'}
            )
        return formfield


@admin.register(TrialBooking)
class TrialBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor']


@admin.register(HourlyBooking)
class HourlyBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor']


@admin.register(PackageBooking)
class PackageBookingAdmin(_BaseBookingAdmin):
    list_display = ['name', 'email', 'mentor', 'package']
