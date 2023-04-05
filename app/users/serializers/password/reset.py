from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class POSTUsersPasswordResetSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['email']
