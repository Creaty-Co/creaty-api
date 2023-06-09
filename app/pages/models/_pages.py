from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from app.base.models.base import BaseModel

__all__ = ['PageMentors', 'Page']


class PageMentors(BaseModel):
    page = models.ForeignKey('Page', models.CASCADE, 'page_mentors')
    mentor = models.ForeignKey('mentors.Mentor', models.CASCADE, 'page_mentors')
    index = models.PositiveSmallIntegerField(validators=[MaxValueValidator(19)])

    class Meta:
        db_table = 'page_mentors'


class Page(BaseModel):
    tag = models.ForeignKey('tags.Tag', models.CASCADE, 'pages', blank=True, null=True)
    category = models.ForeignKey(
        'tags.Category', models.CASCADE, 'pages', blank=True, null=True
    )
    mentors = models.ManyToManyField('mentors.Mentor', 'pages', through=PageMentors)
    tags = models.ManyToManyField('tags.Tag', 'pages_by_tags')

    def clean(self):
        super().clean()
        if self.tag is not None and self.category is not None:
            raise ValidationError(
                "This page has a tag and a category set at the same time"
            )
        from app.pages.services.page import PageService

        max_tags = PageService.MAX_TAGS_COUNT
        if self.id is not None and self.tags.count() > max_tags:
            raise ValidationError(f"There can be no more tags {max_tags}")

    def __str__(self):
        return f"Page: {self.tag or self.category}"
