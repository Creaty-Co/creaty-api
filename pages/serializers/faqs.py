from rest_framework import serializers

from pages.models import Faq


class ListPagesFaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id', 'question', 'answer']


class CreatePagesFaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'question': wo, 'answer': wo}
        fields = list(extra_kwargs.keys())


class PagesFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'question': wo, 'answer': wo}
        fields = list(extra_kwargs.keys())
