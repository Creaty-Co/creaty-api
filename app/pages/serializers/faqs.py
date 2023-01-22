from app.base.serializers.base import BaseModelSerializer
from app.pages.models import Faq


class ListPagesFaqsSerializer(BaseModelSerializer):
    class Meta:
        model = Faq
        fields = ['id', 'question', 'answer']


class CreatePagesFaqsSerializer(BaseModelSerializer):
    class Meta:
        model = Faq
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'question': wo, 'answer': wo}
        fields = list(extra_kwargs.keys())


class PagesFaqSerializer(BaseModelSerializer):
    class Meta:
        model = Faq
        wo = {'write_only': True}
        extra_kwargs = {'question': wo, 'answer': wo}
        fields = list(extra_kwargs.keys())
