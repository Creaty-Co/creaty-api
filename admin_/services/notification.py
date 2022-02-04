from django.core.mail import send_mail

from account.models import User
from forms.models import Application
from forms.models.choices import ReverseFormType, ReverseFormField


class AdminNotificationService:
    @staticmethod
    def _get_admins() -> list[str]:
        return list(User.objects.filter(is_staff=True, email__isnull=False).values_list(
            'email', flat=True
        ))
    
    def _send_admin_emails(self, subject: str, message: str):
        send_mail(subject, message, None, [self._get_admins()])
    
    def on_application(self, application: Application):
        str_fields = '\n'.join(
            f'{ReverseFormField[field].label}: {getattr(application, field)}' for field in
            application.form.fields
        )
        self._send_admin_emails(
            'Пришла заявка',
            f'''Заявка: {ReverseFormType[application.form.type].label}\n{str_fields}'''
        )
    
    def on_subscriber(self, subscriber):
        self._send_admin_emails(
            'Подписка на рассылку',
            f'''Пользователь с email {subscriber.email} подписался на рассылку'''
        )
