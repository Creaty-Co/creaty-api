from django.db.models import Prefetch, Q
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin

from base.views.base import BaseView
from pages.models import Page
from pages.serializers.detail import PageSerializer
from tags.models import Tag


class PageView(RetrieveModelMixin, BaseView):
    serializer_classes = {'get': PageSerializer}
    queryset = Page.objects.prefetch_related(
        'tag', 'category',
        Prefetch('tag_set', queryset=Tag.objects.order_by('page_tag_set__index')),
        Prefetch('mentor_set', queryset=Tag.objects.order_by('page_mentor_set__index')),
    )
    
    def get(self, request, **_):
        return self.retrieve(request)
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        page = get_object_or_404(
            queryset, Q(tag_set__shortcut=self.kwargs['shortcut']) | Q(
                category_set__shortcut=self.kwargs['shortcut']
            )
        )
        self.check_object_permissions(self.request, page)
        return page
