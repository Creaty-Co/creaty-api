from django.db.models import Count

from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.tags.models import Tag
from app.tags.serializers.general import ListTagsSerializer


class TagsView(BaseView):
    many = True
    serializer_map = {'get': ListTagsSerializer}
    queryset = Tag.objects.all()

    def get(self):
        return self.list()

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.annotate(Count('mentor')).exclude(mentor__count=0)
