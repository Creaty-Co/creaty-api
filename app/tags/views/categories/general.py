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
        Category.objects.annotate(
            tags_count=models.Count(
                'tags', filter=models.Q(tags__mentors__isnull=False)
            ),
        )
        .exclude(tags_count=0)
        .prefetch_related(
            models.Prefetch('tags', queryset=Tag.objects.filter(mentors__isnull=False))
        )
    )

    def get(self):
        return self.list()

    def post(self):
        return self.create()
