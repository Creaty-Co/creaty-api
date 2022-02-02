from django.db.models import F
from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from mentors.filters.general import MentorsFilterSet
from mentors.models import Mentor
from mentors.serializers.general import MentorsSerializer


class MentorsView(ListModelMixin, BaseView):
    serializer_classes = {'get': MentorsSerializer}
    queryset = Mentor.objects.annotate(
        country_flag=F('country__flag_unicode')
    ).prefetch_related('tag_set')
    filterset_class = MentorsFilterSet
    
    def get(self, request):
        return self.list(request)
