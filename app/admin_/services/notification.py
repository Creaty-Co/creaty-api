from django.core.mail import send_mail

from app.forms.models import Application
from app.forms.models.choices import rFormType
from app.users.models import User


class AdminNotificationService:
    def __init__(self):
        self.fields = ['path', 'name', 'email', 'about', 'link', 'created_at']

    @staticmethod
    def _get_admins() -> list[str]:
        return list(
            User.objects.filter(is_superuser=True).values_list('email', flat=True)
        )

    def _send_admin_emails(self, subject: str, message: str):
        send_mail(subject, message, None, self._get_admins())

    def on_application(self, application: Application):
        str_fields = '\n'.join(
            f"{field}: {getattr(application, field)}" for field in self.fields
        )
        self._send_admin_emails(
            "Пришла заявка",
            f'''Заявка: {rFormType[application.form.type].label}\n{str_fields}

URL: {application.url}''',
        )

    def on_subscriber(self, subscriber):
        self._send_admin_emails(
            "Подписка на рассылку",
            f'''Пользователь с email {subscriber.email} подписался на рассылку''',
        )
