from django.db.models import Prefetch, Q
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin

from base.views.base import BaseView
from mentors.views import MentorsView
from pages.models import Page
from pages.serializers.personal import PagesPersonalSerializer
from pages.services.page import PageService
from tags.models import Category, Tag


class PagesPersonalView(RetrieveModelMixin, BaseView):
    serializer_classes = {'get': PagesPersonalSerializer}
    queryset = Page.objects.prefetch_related(
        'tag', 'category',
        Prefetch('tag_set', queryset=Tag.objects.order_by('pagetagset__index')),
        Prefetch(
            'mentor_set', queryset=MentorsView.queryset.order_by('pagementorset__index')
        )
    )
    
    def get(self, request, **_):
        return self.retrieve(request)
    
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
                raise
            page = PageService().get_or_create(tag_or_category)
        self.check_object_permissions(self.request, page)
        return page
