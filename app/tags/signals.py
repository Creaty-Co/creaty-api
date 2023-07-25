from django.db.models.signals import m2m_changed, post_delete, post_save

from app.base.utils.decorators import receiver
from app.pages.services.page import PageService
from app.tags.models import Category, Tag
from app.tags.views import TagsCategoriesView


@receiver(post_save, sender=Tag)
def tag_post_save(created, instance, **_):
    TagsCategoriesView.invalidate_list_cache()
    if created:
        tag = instance
        PageService().get_or_create(tag)


@receiver(post_delete, sender=Tag)
def tag_post_delete(**_):
    TagsCategoriesView.invalidate_list_cache()


@receiver(m2m_changed, sender=Tag.categories.through)
def tags_categories_change(**_):
    TagsCategoriesView.invalidate_list_cache()


@receiver(post_save, sender=Category)
def category_post_save(created, instance, **_):
    TagsCategoriesView.invalidate_list_cache()
    if created:
        category = instance
        PageService().get_or_create(category)


@receiver(post_delete, sender=Category)
def category_post_delete(**_):
    TagsCategoriesView.invalidate_list_cache()
