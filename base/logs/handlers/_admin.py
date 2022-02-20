import re
from logging import Formatter

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.log import AdminEmailHandler as DjangoAdminEmailHandler

__all__ = ['AdminEmailHandler']


class AdminEmailHandler(DjangoAdminEmailHandler):
    datefmt = '[%d.%m-%H:%M:%S]'
    
    def __init__(self, include_html=False, email_backend=None, reporter_class=None):
        super().__init__(include_html, email_backend, reporter_class)
        self.record = None
    
    @staticmethod
    def get_admins(level: str) -> set[str]:
        if not settings.LOG_ADMINS:
            return set()
        admins = set()
        for email, levels in settings.LOG_ADMINS.items():
            if level.lower() in levels:
                admins.add(email)
        return admins
    
    def emit(self, record):
        self.record = record
        return super().emit(record)
    
    def create_subject(self):
        record = self.record
        asctime = Formatter().formatTime(record, datefmt=self.datefmt)
        subject = f'{record.levelname} {asctime}: {record.getMessage()}'
        subject = re.sub(' {2,}', ' ', subject.replace('\n', ' ').replace('\t', ' '))
        return subject
    
    def send_mail(self, _, message, fail_silently=True, html_message=None):
        record = self.record
        admins = self.get_admins(record.levelname)
        if not admins:
            return
        mail = EmailMultiAlternatives(
            '%s%s' % (settings.EMAIL_SUBJECT_PREFIX, self.create_subject()), message,
            settings.SERVER_EMAIL, list(admins), connection=self.connection()
        )
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
