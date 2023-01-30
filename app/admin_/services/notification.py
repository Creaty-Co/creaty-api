from django.core.mail import send_mail

from app.forms.models import Application
from app.forms.models.choices import rFormField, rFormType
from app.users.enums.roles import UserRole
from app.users.models import User


class AdminNotificationService:
    @staticmethod
    def _get_admins() -> list[str]:
        return list(
            User.objects.filter(
                role__gte=UserRole.ADMIN, email__isnull=False
            ).values_list('email', flat=True)
        )

    def _send_admin_emails(self, subject: str, message: str):
        send_mail(subject, message, None, self._get_admins())

    def on_application(self, application: Application):
        str_fields = '\n'.join(
            f'{rFormField[field].label}: {getattr(application, field)}'
            for field in [f.type for f in application.form.field_set.all()]
        )
        self._send_admin_emails(
            'Пришла заявка',
            f'''Заявка: {rFormType[application.form.type].label}\n{str_fields}

URL: {application.url}''',
        )

    def on_subscriber(self, subscriber):
        self._send_admin_emails(
            'Подписка на рассылку',
            f'''Пользователь с email {subscriber.email} подписался на рассылку''',
        )
