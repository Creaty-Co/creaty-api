from base.filters.base import ArrayFilter, BaseFilterSet, forms
from mentors.models import Mentor


class MentorsFilterSet(BaseFilterSet):
    tag_set__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_tag_set__in', label='Tag set в'
    )

    class Meta:
        model = Mentor
        fields = {}

    @staticmethod
    def filter_tag_set__in(queryset, name, value):
        return queryset.filter(**{name: value}).distinct()
