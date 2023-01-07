from django.conf import settings
from django.core.mail import EmailMessage

from app.base.logs.handlers import AdminEmailHandler
from app.base.serializers.front.error import BaseFrontErrorSerializer
from app.base.utils.common import response_204
from app.base.views.base import BaseView


class BaseFrontErrorView(BaseView):
    serializer_classes = {'post': BaseFrontErrorSerializer}

    @response_204
    def post(self, request):
        admins = AdminEmailHandler.get_admins('error')
        if not admins:
            return
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        mail = EmailMessage(
            settings.EMAIL_SUBJECT_PREFIX + serializer.validated_data['subject'],
            serializer.validated_data['body'],
            settings.SERVER_EMAIL,
            list(admins),
        )
        mail.send()
