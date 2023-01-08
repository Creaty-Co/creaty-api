from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Tag
from app.tags.serializers.detail import UpdateTagSerializer


class TagView(BaseView):
    serializer_map = {'patch': UpdateTagSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Tag.objects.all()

    def patch(self):
        return self.update()

    def delete(self):
        return self.destroy()
