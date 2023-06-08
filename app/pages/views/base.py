from django.db.models import Count, Prefetch

from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.mentors.views import MentorsView
from app.pages.models import Page
from app.pages.services.page import PageService
from app.tags.models import Tag


class BaseMainPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        Prefetch(
            'mentor_set', queryset=MentorsView.queryset.order_by('pagementorset__index')
        )
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_set_prefetch_qs = Tag.objects.order_by('?').nocache()
        if AdminPermission().has_permission(self.request, self):
            tag_set_prefetch_qs = tag_set_prefetch_qs.annotate(
                Count('mentors')
            ).exclude(mentors__count=0)
        return queryset.prefetch_related(
            Prefetch('tag_set', queryset=tag_set_prefetch_qs)
        )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        main_page = queryset.first()
        if main_page is None:
            main_page = PageService().main
        self.check_object_permissions(self.request, main_page)
        return main_page
