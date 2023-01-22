from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.base.serializers.base import BaseModelSerializer
from app.mentors.models import Mentor
from app.mentors.serializers.general import ListMentorsSerializer
from app.pages.models import Page, PageMentorSet
from app.pages.services.page import PageService
from app.tags.models import Tag
from app.tags.serializers.general import ListTagsSerializer


class PagesRetrieveMainSerializer(BaseModelSerializer):
    tags = ListTagsSerializer(many=True, source='tag_set')
    mentors = ListMentorsSerializer(many=True, source='mentor_set')

    class Meta:
        model = Page
        fields = ['id', 'tags', 'mentors']


class PagesUpdateMainSerializer(BaseModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tag_set', write_only=True
    )
    mentors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Mentor.objects.all(), source='mentor_set', write_only=True
    )

    class Meta:
        model = Page
        fields = ['tags', 'mentors']

    def validate(self, attrs):
        if tags := attrs.get('tag_set'):
            max_tags = PageService.MAX_TAGS_COUNT
            if len(tags) > max_tags:
                raise ValidationError(
                    f'Тегов на странице не может быть больше {max_tags}'
                )
        if mentors := attrs.get('mentor_set'):
            max_mentors = PageService.MENTORS_COUNT
            if len(mentors) > max_mentors:
                raise ValidationError(
                    f'Менторов на странице не может быть больше {max_mentors}'
                )
        return attrs

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_set', None)
        mentors = validated_data.pop('mentor_set', None)
        main_page = super().update(instance, validated_data)
        if tags is not None:
            main_page.tag_set.set(tags)
        if mentors is not None:
            PageMentorSet.objects.filter(page=main_page).delete()
            for index, mentor in enumerate(mentors):
                PageMentorSet.objects.create(page=main_page, index=index, mentor=mentor)
        return main_page
