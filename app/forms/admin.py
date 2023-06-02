from django import forms
from django.contrib import admin
from django.db import models

from app.forms.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'form',
        'path',
        'name',
        'email',
        'telegram',
        'facebook',
        'whats_app',
        'viber',
        'about',
        'url_display',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput(attrs={'size': '20'})}
    }

    def url_display(self, obj):
        return obj.url

    url_display.short_description = 'URL'
