from django.db.models.signals import post_save

from app.admin_.services.notification import AdminNotificationService
from app.base.utils.decorators import receiver
from app.mailings.models import Subscriber


@receiver(post_save, sender=Subscriber)
def mailings_subscriber_post_save(signal, **kwargs):
    _ = signal
    if kwargs['created']:
        subscriber = kwargs['instance']
        AdminNotificationService().on_subscriber(subscriber)
