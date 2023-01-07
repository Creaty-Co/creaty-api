from app.admin_.permissions import AdminPermission
from app.admin_.serializers.mentors import ListAdminMentorsSerializer
from app.base.views.base import BaseView
from app.mentors.models import Mentor


class AdminMentorsView(BaseView):
    many = True
    serializer_map = {'get': ListAdminMentorsSerializer}
    permissions_map = {'get': [AdminPermission]}
    queryset = Mentor.objects.prefetch_related('page_set')

    def get(self):
        return self.list()
