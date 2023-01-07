from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_filters import rest_framework as filters
from django_filters.rest_framework.filters import Filter


class ArrayFilter(Filter):
    field_class = SimpleArrayField


class IntegerFilter(filters.NumberFilter):
    field_class = forms.IntegerField
