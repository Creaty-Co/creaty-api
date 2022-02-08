from rest_framework.mixins import RetrieveModelMixin

from base.views.base import BaseView
from mentors.models import Mentor
from mentors.serializers.detail import MentorSerializer


class MentorView(RetrieveModelMixin, BaseView):
    serializer_classes = {'get': MentorSerializer}
    queryset = Mentor.objects.all()
    
    def get(self, request, **_):
        return self.retrieve(request)
