from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Category
from app.tags.serializers.categories.detail import TagsCategorySerializer


class TagsCategoryView(BaseView):
    serializer_map = {'patch': TagsCategorySerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Category.objects.all()

    def patch(self):
        return self.update()

    def delete(self):
        return self.destroy()
