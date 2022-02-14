from django.db.models import Max
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from base.utils.decorators import schema_response_204
from base.views.base import BaseView
from mentors.models import Mentor
from pages.models import Page, PageMentorSet
from pages.serializers.persoanls.mentor import UpdatePagesPersonalMentorSerializer
from pages.services.page import PageService


class PagesPersonalMentorView(BaseView):
    lookup_url_kwarg = 'page_id'
    serializer_classes = {'patch': UpdatePagesPersonalMentorSerializer}
    queryset = Page.objects.all()
    
    def patch(self, request, **kwargs):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor = get_object_or_404(Mentor, id=kwargs['mentor_id'])
        index = PageMentorSet.objects.filter(page=page).aggregate(Max('index'))[
                    'index__max'
                ] + 1
        if index == PageService.MAX_MENTORS_COUNT:
            raise serializer.WARNINGS[409]
        PageMentorSet.objects.create(page=page, mentor=mentor, index=index)
        return Response(serializer.data)
    
    @schema_response_204
    def delete(self, request, **kwargs):
        page = self.get_object()
        mentor = get_object_or_404(Mentor, id=kwargs['mentor_id'])
        page__mentor = get_object_or_404(PageMentorSet, page=page, mentor=mentor)
        page__mentor.delete()
        for index in range(page__mentor.index + 1, PageService.MAX_MENTORS_COUNT):
            try:
                next_page__mentor = PageMentorSet.objects.get(
                    page=page, mentor=mentor, index=index
                )
            except PageMentorSet.DoesNotExist:
                break
            next_page__mentor.index -= 1
            next_page__mentor.save()
