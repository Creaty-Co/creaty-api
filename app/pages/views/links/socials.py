from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.pages.models import SocialLink
from app.pages.serializers.links.socials import (
    CreatePagesLinksSocialsSerializer,
    ListPagesLinksSocialsSerializer,
    PagesLinksSocialSerializer,
)


class PagesLinksSocialsView(BaseView):
    many = True
    serializer_map = {
        'get': ListPagesLinksSocialsSerializer,
        'post': CreatePagesLinksSocialsSerializer,
    }
    permissions_map = {'post': [AdminPermission]}
    queryset = SocialLink.objects.all()

    def get(self):
        return self.list()

    def post(self):
        return self.create()


class PagesLinksSocialView(BaseView):
    serializer_map = {'patch': PagesLinksSocialSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = SocialLink.objects.all()

    def patch(self):
        return self.update()

    def delete(self):
        return self.destroy()
