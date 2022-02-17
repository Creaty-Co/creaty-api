from django.db.models import Prefetch

from base.views.base import BaseView
from mentors.views import MentorsView
from pages.models import Page
from pages.services.page import PageService
from tags.models import Tag


class BaseMainPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        Prefetch('tag_set', queryset=Tag.objects.order_by('?').nocache()),
        Prefetch(
            'mentor_set', queryset=MentorsView.queryset.order_by('pagementorset__index')
        )
    )
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        main_page = queryset.first()
        if main_page is None:
            main_page = PageService().main
        self.check_object_permissions(self.request, main_page)
        return main_page
