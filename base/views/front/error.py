from django.conf import settings
from django.core.mail import EmailMessage

from base.logs.handlers import AdminEmailHandler
from base.serializers.front.error import BaseFrontErrorSerializer
from base.utils.decorators import schema_response_204
from base.views.base import BaseView


class BaseFrontErrorView(BaseView):
    serializer_classes = {'post': BaseFrontErrorSerializer}

    @schema_response_204
    def post(self, request):
        admins = AdminEmailHandler.get_admins('error')
        if not admins:
            return
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail = EmailMessage(
            settings.EMAIL_SUBJECT_PREFIX + serializer.validated_data['subject'],
            serializer.validated_data['body'],
            settings.SERVER_EMAIL,
            list(admins),
        )
        mail.send()
