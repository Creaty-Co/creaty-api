from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class GETUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        read_only_fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'has_discount',
            'is_verified',
            'is_staff',
            'is_mentor',
        ]


class PATCHUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['first_name', 'last_name']
