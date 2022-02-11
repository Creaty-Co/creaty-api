from rest_framework import serializers

from mentors.models import Mentor
from mentors.serializers.general import ListMentorsSerializer
from pages.models import Page, PageMentorSet, PageTagSet
from tags.models import Tag
from tags.serializers.general import ListTagsSerializer


class PagesRetrieveMainSerializer(serializers.ModelSerializer):
    tags = ListTagsSerializer(many=True, source='tag_set')
    mentors = ListMentorsSerializer(many=True, source='mentor_set')
    
    class Meta:
        model = Page
        fields = ['id', 'tags', 'mentors']


class PagesUpdateMainSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tag_set', write_only=True
    )
    mentors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Mentor.objects.all(), source='mentor_set', write_only=True
    )
    
    class Meta:
        model = Page
        fields = ['id', 'tags', 'mentors']
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_set', None)
        mentors = validated_data.pop('mentor_set', None)
        main_page = super().update(instance, validated_data)
        if tags is not None:
            PageTagSet.objects.filter(page=main_page).delete()
            for index, tag in enumerate(tags):
                PageTagSet.objects.create(page=main_page, index=index, tag=tag)
        if mentors is not None:
            PageMentorSet.objects.filter(page=main_page).delete()
            for index, mentor in enumerate(mentors):
                PageMentorSet.objects.create(page=main_page, index=index, mentor=mentor)
        return main_page
