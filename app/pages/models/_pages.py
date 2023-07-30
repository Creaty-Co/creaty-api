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
        constraints = [
            models.UniqueConstraint(
                fields=['page', 'mentor'], name='unique_page_mentor'
            ),
            models.UniqueConstraint(fields=['page', 'index'], name='unique_page_index'),
        ]

    def __str__(self):
        return f"{self.page} ↔ {self.mentor} ({self.index})"


class Page(BaseModel):
    tag = models.OneToOneField('tags.Tag', models.CASCADE, blank=True, null=True)
    category = models.OneToOneField(
        'tags.Category', models.CASCADE, blank=True, null=True
    )
    mentors = models.ManyToManyField('mentors.Mentor', 'pages', through=PageMentors)
    tags = models.ManyToManyField('tags.Tag', 'pages_by_tags')

    def clean(self):
        super().clean()
        if self.tag is not None and self.category is not None:
            raise ValidationError(
                "This page has a tag and a category set at the same time"
            )

    def __str__(self):
        return f"Page: {self.tag or self.category or 'main'}"
