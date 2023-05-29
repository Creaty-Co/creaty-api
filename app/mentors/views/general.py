from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.mentors.filters.general import MentorsFilterSet
from app.mentors.models import Mentor
from app.mentors.serializers.general import GETMentorsSerializer, POSTMentorsSerializer


class MentorsView(BaseView):
    many = True
    serializer_map = {'get': GETMentorsSerializer, 'post': POSTMentorsSerializer}
    permissions_map = {'post': [AdminPermission]}
    queryset = Mentor.objects.prefetch_related('tag_set', 'country')
    filterset_class = MentorsFilterSet

    def get(self):
        return self.list()

    def post(self):
        return self.create()

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.filter(is_draft=False)
