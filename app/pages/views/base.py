from django.db.models import Prefetch

from app.base.views import BaseView
from app.mentors.views import MentorsView
from app.pages.models import Page
from app.pages.services.page import PageService
from app.tags.models import Tag


class BaseMainPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        Prefetch(
            'mentors',
            queryset=MentorsView.queryset.filter(is_draft=False).order_by(
                'page_mentors__index'
            ),
        ),
        Prefetch(
            'tags', queryset=Tag.objects.filter(mentors__isnull=False).order_by('?')
        ),
    )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        main_page = queryset.first()
        if main_page is None:
            main_page = PageService().main
        self.check_object_permissions(self.request, main_page)
        return main_page
