from django import forms
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.forms import SimpleArrayField
from django_filters import filterset, rest_framework as filters
from django_filters.rest_framework.filters import Filter


class ArrayFilter(Filter):
    field_class = SimpleArrayField


class IntegerFilter(filters.NumberFilter):
    field_class = forms.IntegerField


class BaseFilterSet(filters.FilterSet):
    FILTER_DEFAULTS = filterset.FILTER_FOR_DBFIELD_DEFAULTS | {
        ArrayField: {'filter_class': ArrayFilter}
    }
