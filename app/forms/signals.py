from django.db.models.signals import post_save

from app.admin_.services.notification import AdminNotificationService
from app.base.utils.decorators import receiver
from app.forms.models import Application


@receiver(post_save, sender=Application)
def forms_application_post_save(signal, **kwargs):
    _ = signal
    if kwargs['created']:
        application = kwargs['instance']
        AdminNotificationService().on_application(application)
