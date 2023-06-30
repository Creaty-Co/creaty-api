from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Tag
from app.tags.serializers.general import ListTagsSerializer, POSTTagsSerializer


class TagsView(BaseView):
    many = True
    permissions_map = {'post': [AdminPermission]}
    serializer_map = {'get': ListTagsSerializer, 'post': POSTTagsSerializer}
    queryset = Tag.objects.filter(mentors__is_draft=False)

    def get(self):
        return self.list()

    def post(self):
        return self.create()
