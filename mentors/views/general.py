from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from mentors.filters.general import MentorsFilterSet
from mentors.models import Mentor
from mentors.serializers.general import MentorsSerializer


# TODO: #37
class MentorsView(ListModelMixin, BaseView):
    serializer_classes = {'get': MentorsSerializer}
    queryset = Mentor.objects.prefetch_related('tag_set', 'country')
    filterset_class = MentorsFilterSet
    
    def get(self, request):
        return self.list(request)
