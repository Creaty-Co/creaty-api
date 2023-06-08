from app.base.views import BaseView
from app.mentors.models import Mentor
from app.mentors.serializers.detail import RetrieveMentorSerializer


class MentorView(BaseView):
    serializer_map = {'get': RetrieveMentorSerializer}
    lookup_field = 'slug'
    queryset = Mentor.objects.filter(is_draft=False)

    def get(self):
        return self.retrieve()
