from rest_framework.mixins import (
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from mentors.models import Mentor
from mentors.serializers.detail import RetrieveMentorSerializer, UpdateMentorSerializer


class MentorView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, BaseView):
    serializer_classes = {
    'get': RetrieveMentorSerializer,
    'patch': UpdateMentorSerializer,
}
    permission_classes_map = {
    'patch': BaseAdminView.permission_classes,
    'delete': BaseAdminView.permission_classes,
}
    queryset = Mentor.objects.all()

    def get(self, request, **_):
        return self.retrieve(request)

    def patch(self, request, **_):
        return self.partial_update(request)

    def delete(self, request, **_):
        return self.destroy(request)
