from django.core.mail import get_connection
from rest_framework import serializers
from rest_framework.response import Response

from app.admin_.permissions import AdminPermission
from app.base.utils.schema import schema_serializer
from app.base.views import BaseView
from app.mailings.models import Mailing, Subscriber
from app.mailings.services.email import MailingEmailMessage


class MailingSendView(BaseView):
    serializer_class = schema_serializer(
        'AdminMailingSend', id=serializers.IntegerField(read_only=True)
    )
    permissions_map = {'post': [AdminPermission]}
    queryset = Mailing.objects.all()

    def post(self, request, **_):
        mailing = self.get_object()
        connection = get_connection()
        messages = []
        for subscriber in Subscriber.objects.all():
            message = MailingEmailMessage(
                mailing, subscriber, connection=connection, request=request
            )
            message.render()
            messages.append(message)
        mailing.task_ids = [r.id for r in connection.send_messages(messages)]
        mailing.save()
        return Response({'id': mailing.id})
