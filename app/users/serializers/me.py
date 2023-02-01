from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class GETUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class PATCHUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['first_name', 'last_name']
