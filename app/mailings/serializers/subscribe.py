from app.base.serializers.base import BaseModelSerializer
from app.mailings.models import Subscriber


class MailingsSubscribeSerializer(BaseModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email']
