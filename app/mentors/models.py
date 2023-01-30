from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from uuslug import uuslug

from app.base.models.base import BaseModel
from app.base.money import Money
from app.geo.models import *
from app.tags.models import Tag

__all__ = ['Mentor', 'Package', 'MentorInfo']


class Mentor(BaseModel):
    info = models.OneToOneField('MentorInfo', models.CASCADE)
    slug = models.SlugField(unique=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    profession = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    price: Money = MoneyField(max_digits=10, decimal_places=2)
    tag_set = models.ManyToManyField(Tag)
    country = models.ForeignKey(Country, models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug(f"{self.first_name}_{self.last_name}", self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.info:
            self.info.delete()


class Package(BaseModel):
    mentor = models.ForeignKey(Mentor, models.CASCADE, related_name='packages')
    lessons_count = models.SmallIntegerField(validators=[MinValueValidator(2)])
    discount = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )


class MentorInfo(BaseModel):
    trial_meeting = models.SmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    resume = models.TextField()
    what_help = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    language_set = models.ManyToManyField(Language)
    city = models.TextField(null=True, blank=True)
