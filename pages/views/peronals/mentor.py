from admin_.views import BaseAdminView
from pages.serializers.mentor import UpdatePageMentorSerializer
from pages.views.peronals.base import BasePersonalPageView
from pages.views.mentor import PagesMainMentorView


class PagesPersonalMentorView(BasePersonalPageView, PagesMainMentorView):
    serializer_classes = {'patch': UpdatePageMentorSerializer}
    permission_classes_map = {
        'patch': BaseAdminView.permission_classes,
        'delete': BaseAdminView.permission_classes,
    }

    def get_queryset(self):
        return PagesMainMentorView.get_queryset(self)
