from app.base.exceptions import ClientError
from app.base.serializers.base import BaseModelSerializer
from app.forms.models import Application


class FormApplicationsSerializer(BaseModelSerializer):
    class Meta:
        model = Application
        wo = {'write_only': True}
        extra_kwargs = {
            'path': wo,
            'name': wo,
            'email': wo,
            'telegram': wo,
            'facebook': wo,
            'whats_app': wo,
            'viber': wo,
            'about': wo,
        }
        fields = list(extra_kwargs.keys())

    def validate_path(self, path: str):
        if not path.startswith('/'):
            raise ClientError("`path` should starts with /")
        return path
