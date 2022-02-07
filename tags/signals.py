from django.db.models.signals import post_save

from base.utils.decorators import receiver
from pages.services.page import PageService
from tags.models import Category, Tag


@receiver(post_save, sender=Tag)
def tags_tag_post_save(signal, **kwargs):
    _ = signal
    if kwargs['created']:
        tag = kwargs['instance']
        PageService().get_or_create(tag)


@receiver(post_save, sender=Category)
def tags_category_post_save(signal, **kwargs):
    _ = signal
    if kwargs['created']:
        category = kwargs['instance']
        PageService().get_or_create(category)
