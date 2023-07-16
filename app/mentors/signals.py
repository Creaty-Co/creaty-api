from django.db.models.signals import m2m_changed, post_delete, post_save

from app.base.utils.decorators import receiver
from app.mentors.models import Mentor
from app.tags.views import TagsCategoriesView


@receiver(post_save, sender=Mentor)
def mentor_post_save(**_):
    TagsCategoriesView.invalidate_list_cache()


@receiver(post_delete, sender=Mentor)
def mentor_post_delete(**_):
    TagsCategoriesView.invalidate_list_cache()


@receiver(m2m_changed, sender=Mentor.tags.through)
def mentor_tags_change(**_):
    TagsCategoriesView.invalidate_list_cache()
