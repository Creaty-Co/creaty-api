from drf_base64.fields import Base64FileField

from base.serializers.base import BaseSerializer


class BaseXlsxSerializer(BaseSerializer):
    xlsx = Base64FileField(write_only=True)
