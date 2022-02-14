from django.db.models import Max
from rest_framework.response import Response

from base.views.base import BaseView
from pages.models import Page, PageMentorSet
from pages.serializers.persoanls.mentors import UpdatePagesPersonalMentorsSerializer
from pages.services.page import PageService


class PagesPersonalMentorsView(BaseView):
    serializer_classes = {'patch': UpdatePagesPersonalMentorsSerializer}
    queryset = Page.objects.all()
    
    def patch(self, request, **_):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor = serializer.validated_data['mentor']
        index = PageMentorSet.objects.filter(page=page).aggregate(Max('index'))[
            'index__max'
        ] + 1
        if index == PageService.MAX_MENTORS_COUNT:
            raise serializer.WARNINGS[409]
        PageMentorSet.objects.create(page=page, mentor=mentor, index=index)
        return Response(serializer.data)
