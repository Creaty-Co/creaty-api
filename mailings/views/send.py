from django.core.mail import get_connection
from rest_framework import serializers
from rest_framework.response import Response

from admin_.views.base import BaseAdminView
from base.utils.functions import schema_serializer
from mailings.models import Mailing, Subscriber
from mailings.services.email import MailingEmailMessage


class MailingSendView(BaseAdminView):
    serializer_class = schema_serializer(
        'AdminMailingSend', id=serializers.IntegerField(read_only=True)
    )
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
