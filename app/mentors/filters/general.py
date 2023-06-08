from app.base.filters.base import ArrayFilter, forms
from app.base.filtersets.base import BaseFilterSet
from app.mentors.models import Mentor


# FIXME: tag_set -> tags
class MentorsFilterSet(BaseFilterSet):
    tag_set__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_tag_set__in', label='Tag set в'
    )

    class Meta:
        model = Mentor
        fields = {}

    @staticmethod
    def filter_tag_set__in(queryset, _, value):
        return queryset.filter(**{'tags__in': value}).distinct()
