from django.db.models import Prefetch, Count

from admin_.permissions import IsAdminPermission
from base.views.base import BaseView
from mentors.views import MentorsView
from pages.models import Page
from pages.services.page import PageService
from tags.models import Tag


class BaseMainPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        Prefetch(
            'mentor_set', queryset=MentorsView.queryset.order_by('pagementorset__index')
        )
    )
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_set_prefetch_qs = Tag.objects.order_by('?').nocache()
        if IsAdminPermission().has_permission(self.request, self):
            tag_set_prefetch_qs = tag_set_prefetch_qs.annotate(Count('mentor')).exclude(
                mentor__count=0
            )
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
