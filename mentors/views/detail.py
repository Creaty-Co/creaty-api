from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from mentors.models import Mentor
from mentors.serializers.detail import MentorSerializer


class MentorView(RetrieveModelMixin, DestroyModelMixin, BaseView):
    serializer_classes = {'get': MentorSerializer}
    permission_classes_map = {'delete': BaseAdminView.permission_classes}
    queryset = Mentor.objects.all()
    
    def get(self, request, **_):
        return self.retrieve(request)
    
    def delete(self, request, **_):
        return self.destroy(request)
