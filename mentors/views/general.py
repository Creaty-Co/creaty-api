from rest_framework.mixins import CreateModelMixin, ListModelMixin

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from mentors.filters.general import MentorsFilterSet
from mentors.models import Mentor
from mentors.serializers.general import CreateMentorsSerializer, ListMentorsSerializer


class MentorsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {'get': ListMentorsSerializer, 'post': CreateMentorsSerializer}
    permission_classes_map = {'post': BaseAdminView.permission_classes}
    queryset = Mentor.objects.prefetch_related('tag_set', 'country')
    filterset_class = MentorsFilterSet
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
