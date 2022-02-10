from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from base.models import AbstractModel

__all__ = ['PageMentorSet', 'PageTagSet', 'Page']


class PageMentorSet(AbstractModel):
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE)
    mentor = models.ForeignKey('mentors.Mentor', on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(validators=[MaxValueValidator(19)])
    
    class Meta:
        db_table = 'page_mentor_set'
        constraints = [
            models.UniqueConstraint(
                fields=('page', 'mentor'), name='page_mentor_set__unique__page__mentor'
            ),
            models.UniqueConstraint(
                fields=('page', 'index'), name='page_mentor_set__unique__page__index'
            )
        ]


class PageTagSet(AbstractModel):
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE)
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE)
    index = models.IntegerField()
    
    class Meta:
        db_table = 'page_tag_set'
        constraints = [
            models.UniqueConstraint(
                fields=('page', 'tag'), name='page_tag_set__unique__page__tag'
            ),
            models.UniqueConstraint(
                fields=('page', 'index'), name='page_tag_set__unique__page__index'
            )
        ]


class Page(AbstractModel):
    tag = models.OneToOneField(
        'tags.Tag', on_delete=models.CASCADE, blank=True, null=True
    )
    category = models.OneToOneField(
        'tags.Category', on_delete=models.CASCADE, blank=True, null=True
    )
    mentor_set = models.ManyToManyField('mentors.Mentor', through=PageMentorSet)
    tag_set = models.ManyToManyField(
        'tags.Tag', through=PageTagSet, related_name='page_set_by_tag_set'
    )
    
    def clean(self):
        super().clean()
        if self.tag is not None and self.category is not None:
            raise ValidationError(f'У Page({self.id}) заданы tag и category')
