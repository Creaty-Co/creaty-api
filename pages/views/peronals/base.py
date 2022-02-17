from django.db.models import Prefetch, Q
from django.http import Http404
from rest_framework.generics import get_object_or_404

from base.views.base import BaseView
from mentors.views import MentorsView
from pages.models import Page
from pages.services.page import PageService
from tags.models import Category, Tag


class BasePersonalPageView(BaseView):
    queryset = Page.objects.prefetch_related(
        'tag', 'category',
        Prefetch('tag_set', queryset=Tag.objects.order_by('?').nocache()),
        Prefetch(
            'mentor_set', queryset=MentorsView.queryset.order_by('pagementorset__index')
        )
    )
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        shortcut = self.kwargs['shortcut']
        try:
            page = get_object_or_404(
                queryset,
                Q(tag__shortcut=shortcut) | Q(category__shortcut=shortcut)
            )
        except Http404:
            tag_or_category = Tag.objects.filter(
                shortcut=shortcut
            ).first() or Category.objects.filter(shortcut=shortcut).first()
            if tag_or_category is None:
                if self.request.method.lower() == 'get':
                    page = PageService().main
                else:
                    raise
            else:
                page = PageService().get_or_create(tag_or_category)
        self.check_object_permissions(self.request, page)
        return page
