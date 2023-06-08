from app.base.views import BaseView
from app.mentors.filters.general import MentorsFilterSet
from app.mentors.models import Mentor
from app.mentors.serializers.general import GETMentorsSerializer


class MentorsView(BaseView):
    many = True
    serializer_map = {'get': GETMentorsSerializer}
    queryset = Mentor.objects.filter(is_draft=False).prefetch_related('tags', 'country')
    filterset_class = MentorsFilterSet

    def get(self):
        return self.list()
