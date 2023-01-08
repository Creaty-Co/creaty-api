from app.account.enums.users import UserType
from app.account.models import User
from app.base.serializers.base import BaseModelSerializer


class GET_AccountMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'type': {'help_text': UserType.help_text}}
        fields = ['id', 'email', 'first_name', 'last_name', 'type']


class PATCH_AccountMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['first_name', 'first_name']
