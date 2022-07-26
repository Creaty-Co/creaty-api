from django.db.models import Count
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from admin_.permissions import IsAdminPermission
from base.views.base import BaseView
from tags.models import Tag
from tags.serializers.general import ListTagsSerializer


class TagsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {'get': ListTagsSerializer}
    queryset = Tag.objects.all()

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsAdminPermission().has_permission(self.request, self):
            return queryset
        return queryset.annotate(Count('mentor')).exclude(mentor__count=0)
