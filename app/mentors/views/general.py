from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.mentors.filters.general import MentorsFilterSet
from app.mentors.models import Mentor
from app.mentors.serializers.general import (
    CreateMentorsSerializer,
    ListMentorsSerializer,
)


class MentorsView(BaseView):
    many = True
    serializer_map = {'get': ListMentorsSerializer, 'post': CreateMentorsSerializer}
    permissions_map = {'post': [AdminPermission]}
    queryset = Mentor.objects.prefetch_related('tag_set', 'country')
    filterset_class = MentorsFilterSet

    def get(self):
        return self.list()

    def post(self):
        return self.create()
