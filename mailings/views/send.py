from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Template
from django.template.context import make_context
from rest_framework import serializers
from rest_framework.response import Response

from admin_.views.base import BaseAdminView
from base.utils.functions import schema_serializer
from mailings.models import Mailing, Subscriber


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
            rendered_content = Template(mailing.content).render(
                make_context({'subscriber': subscriber})
            )
            message = EmailMultiAlternatives(
                subject=mailing.subject, body=rendered_content,
                to=[subscriber.email], connection=connection
            )
            message.attach_alternative(rendered_content, 'text/html')
            messages.append(message)
        mailing.task_ids = [r.id for r in connection.send_messages(messages)]
        mailing.save()
        return Response({'id': mailing.id})
