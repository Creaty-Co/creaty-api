from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.tags.models import Category
from app.tags.serializers.categories.detail import TagsCategorySerializer


class TagsCategoryView(BaseView):
    serializer_map = {'patch': TagsCategorySerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Category.objects.all()

    @response_204
    def patch(self):
        self.update()

    def delete(self):
        return self.destroy()
