from django.db import models

from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Category, Tag
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
    queryset = (
        Category.objects.prefetch_related(
            models.Prefetch(
                'tags',
                queryset=Tag.objects.filter(mentors__is_draft=False).distinct(),
            )
        )
        .filter(tags__mentors__is_draft=False)
        .distinct()
    )

    def get(self):
        return self.list()

    def post(self):
        return self.create()
