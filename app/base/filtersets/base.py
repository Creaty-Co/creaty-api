from django.contrib.postgres.fields import ArrayField
from django_filters import filterset
from django_filters import rest_framework as filters

from app.base.filters.base import ArrayFilter


class BaseFilterSet(filters.FilterSet):
    FILTER_DEFAULTS = filterset.FILTER_FOR_DBFIELD_DEFAULTS | {
        ArrayField: {'filter_class': ArrayFilter}
    }
