from django.db.models import Count

from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Category
from app.tags.serializers.categories.general import (
    CreateTagsCategoriesSerializer,
    ListTagsCategoriesSerializer,
)


class TagsCategoriesView(BaseView):
    many = True
    serializer_map = {
        'get': ListTagsCategoriesSerializer,
        'post': CreateTagsCategoriesSerializer,
    }
    permissions_map = {'post': [AdminPermission]}
    queryset = Category.objects.prefetch_related('tags')

    def get(self):
        return self.list()

    def post(self):
        return self.create()

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.annotate(Count('tags'), Count('tags__mentors')).exclude(
            tags__count=0, tags__mentors__count=0
        )
