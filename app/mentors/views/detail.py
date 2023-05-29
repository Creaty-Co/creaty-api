from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.mentors.models import Mentor
from app.mentors.serializers.detail import (
    RetrieveMentorSerializer,
    UpdateMentorSerializer,
)


class MentorView(BaseView):
    serializer_map = {'get': RetrieveMentorSerializer, 'patch': UpdateMentorSerializer}
    lookup_field = 'slug'
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Mentor.objects.all()

    def get(self):
        return self.retrieve()

    @response_204
    def patch(self):
        self.update()

    @response_204
    def delete(self):
        self.destroy()

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.filter(is_draft=False)
