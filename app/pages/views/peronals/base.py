from django.db.models import Prefetch, Q
from django.http import Http404
from rest_framework.generics import get_object_or_404

from app.base.views import BaseView
from app.mentors.views import MentorsView
from app.pages.models import Page
from app.pages.services.page import PageService
from app.tags.models import Category, Tag


class BasePersonalPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        'tag',
        'category',
        Prefetch(
            'mentors',
            queryset=MentorsView.queryset.filter(is_draft=False).order_by(
                'page_mentors__index'
            ),
        ),
    )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        shortcut = self.kwargs['shortcut']
        try:
            page = get_object_or_404(
                queryset, Q(tag__shortcut=shortcut) | Q(category__shortcut=shortcut)
            )
        except Http404:
            tag_or_category = (
                Tag.objects.filter(shortcut=shortcut).first()
                or Category.objects.filter(shortcut=shortcut).first()
            )
            if tag_or_category is None:
                if self.request.method.lower() == 'get':
                    page = PageService().main
                else:
                    raise
            else:
                page = PageService().get_or_create(tag_or_category)
        self.check_object_permissions(self.request, page)
        return page
