from rest_framework.response import Response

from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Category
from app.tags.serializers.categories.tags import TagsCategoryTagsSerializer


class TagsCategoryTagsView(BaseView):
    lookup_url_kwarg = 'category_id'
    serializer_map = {'post': TagsCategoryTagsSerializer}
    permissions_map = {'post': [AdminPermission]}
    queryset = Category.objects.all()

    def post(self):
        serializer = self.get_valid_serializer(data=self.get_data())
        serializer.save(category=self.get_object())
        return Response(serializer.data, status=201)
