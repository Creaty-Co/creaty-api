from django import forms
from django.contrib import admin
from django.db import models

from app.forms.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'form',
        'form_type',
        'path',
        'name',
        'email',
        'telegram',
        'facebook',
        'whats_app',
        'viber',
        'about',
        'url',
    ]
    list_filter = ['form__type']
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput(attrs={'size': '20'})}
    }

    def url(self, obj):
        return obj.url

    def form_type(self, obj):
        return obj.form.type
