from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from app.base.models.base import BaseModel

__all__ = ['PageMentorSet', 'Page']


class PageMentorSet(BaseModel):
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE)
    mentor = models.ForeignKey('mentors.Mentor', on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(validators=[MaxValueValidator(19)])

    class Meta:
        db_table = 'page_mentor_set'


class Page(BaseModel):
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        'tags.Category', on_delete=models.CASCADE, blank=True, null=True
    )
    mentor_set = models.ManyToManyField('mentors.Mentor', through=PageMentorSet)
    tag_set = models.ManyToManyField('tags.Tag', related_name='page_set_by_tag_set')

    def clean(self):
        super().clean()
        if self.tag is not None and self.category is not None:
            raise ValidationError(f'У Page({self.id}) заданы tag и category')
        from app.pages.services.page import PageService

        max_tags = PageService.MAX_TAGS_COUNT
        if self.id is not None and self.tag_set.count() > max_tags:
            raise ValidationError(f'Тегов не может быть больше {max_tags}')
