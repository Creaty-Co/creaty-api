from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
)

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from pages.models import SocialLink
from pages.serializers.links.socials import (
    CreatePagesLinksSocialsSerializer, ListPagesLinksSocialsSerializer,
    PagesLinksSocialSerializer
)


class PagesLinksSocialsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {
        'get': ListPagesLinksSocialsSerializer, 'post': CreatePagesLinksSocialsSerializer
    }
    permission_classes_map = {'post': BaseAdminView.permission_classes}
    queryset = SocialLink.objects.all()
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class PagesLinksSocialView(UpdateModelMixin, DestroyModelMixin, BaseAdminView):
    serializer_classes = {'patch': PagesLinksSocialSerializer}
    queryset = SocialLink.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
    
    def delete(self, request, **_):
        return self.destroy(request)
