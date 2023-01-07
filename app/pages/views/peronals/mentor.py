from app.admin_.permissions import AdminPermission
from app.pages.serializers.mentor import UpdatePageMentorSerializer
from app.pages.views.mentor import PagesMainMentorView
from app.pages.views.peronals.base import BasePersonalPageView


class PagesPersonalMentorView(BasePersonalPageView, PagesMainMentorView):
    serializer_map = {'patch': UpdatePageMentorSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}

    def get_queryset(self):
        return PagesMainMentorView.get_queryset(self)
