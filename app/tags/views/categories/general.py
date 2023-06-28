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
    queryset = Category.objects.prefetch_related('tags').filter(
        tags__isnull=False, tags__mentors__isnull=False
    )

    def get(self):
        return self.list()

    def post(self):
        return self.create()
