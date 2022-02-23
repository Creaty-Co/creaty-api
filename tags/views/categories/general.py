from django.db.models import Count
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from admin_.permissions import IsAdminPermission
from admin_.views import BaseAdminView
from base.views.base import BaseView
from tags.models import Category
from tags.serializers.categories.general import (
    CreateTagsCategoriesSerializer, ListTagsCategoriesSerializer
)


class TagsCategoriesView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {
        'get': ListTagsCategoriesSerializer, 'post': CreateTagsCategoriesSerializer
    }
    permission_classes_map = {'post': BaseAdminView.permission_classes}
    queryset = Category.objects.prefetch_related('tag_set')
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if IsAdminPermission().has_permission(self.request, self):
            return queryset.annotate(Count('tag')).exclude(tag__count=0)
        return queryset
