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
    queryset = Category.objects.prefetch_related('tag_set')

    def get(self):
        return self.list()

    def post(self):
        return self.create()

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.annotate(Count('tag'), Count('tag__mentor')).exclude(
            tag__count=0, tag__mentor__count=0
        )
