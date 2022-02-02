from mentors.models import Mentor
from base.filters.base import *


class MentorsFilterSet(BaseFilterSet):
    class Meta:
        model = Mentor
        fields = {'tag_set': ['exact']}
