from rest_framework.mixins import ListModelMixin

from admin_.serializers.mentors import ListAdminMentorsSerializer
from admin_.views.base import BaseAdminView
from mentors.models import Mentor


class AdminMentorsView(ListModelMixin, BaseAdminView):
    serializer_classes = {'get': ListAdminMentorsSerializer}
    queryset = Mentor.objects.prefetch_related('page_set')

    def get(self, request):
        return self.list(request)
