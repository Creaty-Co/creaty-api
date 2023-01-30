from app.base.serializers.base import BaseModelSerializer
from app.users.enums.roles import UserRole
from app.users.models import User


class GETUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'role': {'help_text': UserRole.help_text}}
        fields = ['id', 'role', 'email', 'first_name', 'last_name']


class PATCHUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['first_name', 'last_name']
