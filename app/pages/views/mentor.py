from django.db.models import Max
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.mentors.models import Mentor
from app.pages.models import PageMentorSet
from app.pages.serializers.mentor import UpdatePageMentorSerializer
from app.pages.services.page import PageService
from app.pages.views import BaseMainPageView


class PagesMainMentorView(BaseMainPageView):
    serializer_map = {'patch': UpdatePageMentorSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}

    def patch(self, request, **kwargs):
        page = self.get_object()
        serializer = self.get_serializer(page, data=request.data)
        serializer.is_valid()
        mentor = get_object_or_404(Mentor, id=kwargs['mentor_id'])
        if not PageMentorSet.objects.filter(page=page, mentor=mentor).exists():
            index = PageMentorSet.objects.filter(page=page).aggregate(Max('index'))[
                'index__max'
            ]
            index = 0 if index is None else index + 1
            if index == PageService.MENTORS_COUNT:
                raise serializer.WARNINGS[409]
            PageMentorSet.objects.create(page=page, mentor=mentor, index=index)
        return Response(serializer.data)

    @response_204
    def delete(self):
        page = self.get_object()
        mentor = get_object_or_404(Mentor, id=self.kwargs['mentor_id'])
        try:
            page__mentor = PageMentorSet.objects.get(page=page, mentor=mentor)
        except PageMentorSet.DoesNotExist:
            return
        page__mentor.delete()
        for index in range(page__mentor.index + 1, PageService.MENTORS_COUNT):
            try:
                next_page__mentor = PageMentorSet.objects.get(page=page, index=index)
            except PageMentorSet.DoesNotExist:
                break
            next_page__mentor.index -= 1
            next_page__mentor.save()
