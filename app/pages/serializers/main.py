import random

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.base.serializers.base import BaseModelSerializer
from app.mentors.models import Mentor
from app.mentors.serializers.general import GETMentorsSerializer
from app.pages.models import Page, PageMentors
from app.pages.services.page import PageService
from app.tags.models import Tag
from app.tags.serializers.general import ListTagsSerializer


class PagesRetrieveMainSerializer(BaseModelSerializer):
    tags = ListTagsSerializer(many=True)
    mentors = GETMentorsSerializer(many=True)

    class Meta:
        model = Page
        read_only_fields = ['id', 'tags', 'mentors']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tags = representation['tags']
        representation['tags'] = random.sample(tags, len(tags))
        return representation


class PagesUpdateMainSerializer(BaseModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True
    )
    mentors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Mentor.objects.all(), write_only=True
    )

    class Meta:
        model = Page
        fields = ['tags', 'mentors']

    def validate(self, attrs):
        if tags := attrs.get('tags'):
            max_tags = PageService.MAX_TAGS_COUNT
            if len(tags) > max_tags:
                raise ValidationError(
                    f'Тегов на странице не может быть больше {max_tags}'
                )
        if mentors := attrs.get('mentors'):
            max_mentors = PageService.MENTORS_COUNT
            if len(mentors) > max_mentors:
                raise ValidationError(
                    f'Менторов на странице не может быть больше {max_mentors}'
                )
        return attrs

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        mentors = validated_data.pop('mentors', None)
        main_page = super().update(instance, validated_data)
        if tags is not None:
            main_page.tags.set(tags)
        if mentors is not None:
            PageMentors.objects.filter(page=main_page).delete()
            for index, mentor in enumerate(mentors):
                PageMentors.objects.create(page=main_page, index=index, mentor=mentor)
        return main_page
