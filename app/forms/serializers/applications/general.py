from app.base.exceptions import ClientError
from app.base.serializers.base import BaseModelSerializer
from app.forms.models import Application


class FormApplicationsSerializer(BaseModelSerializer):
    class Meta:
        model = Application
        write_only_fields = [
            'path',
            'name',
            'email',
            'telegram',
            'facebook',
            'whats_app',
            'viber',
            'about',
            'link',
        ]

    def validate_path(self, path: str):
        if not path.startswith('/'):
            raise ClientError("`path` should starts with /")
        return path
