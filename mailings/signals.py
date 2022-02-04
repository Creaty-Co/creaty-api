from django.db.models.signals import post_save

from admin_.services.notification import AdminNotificationService
from base.utils.decorators import receiver
from mailings.models import Subscribe


@receiver(post_save, sender=Subscribe)
def mailings_subscribe_post_save(signal, **kwargs):
    _ = signal
    if kwargs['created']:
        subscribe = kwargs['instance']
        AdminNotificationService().on_subscribe(subscribe)
