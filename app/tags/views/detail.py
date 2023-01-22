from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.tags.models import Tag
from app.tags.serializers.detail import UpdateTagSerializer


class TagView(BaseView):
    serializer_map = {'patch': UpdateTagSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Tag.objects.all()

    @response_204
    def patch(self):
        self.update()

    def delete(self):
        return self.destroy()
