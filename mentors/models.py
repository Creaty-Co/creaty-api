from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField

from base.models import AbstractModel
from base.money import Money
from geo.models import *
from tags.models import Tag

__all__ = ['Mentor', 'Package', 'MentorInfo']


class Mentor(AbstractModel):
    info = models.OneToOneField('MentorInfo', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    company = models.TextField(null=True, blank=True)
    profession = models.TextField(null=True, blank=True)
    first_name = models.TextField()
    last_name = models.TextField()
    price: Money = MoneyField(max_digits=10, decimal_places=2)
    tag_set = models.ManyToManyField(Tag)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)


class Package(AbstractModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    lessons_count = models.SmallIntegerField(validators=[MinValueValidator(2)])
    discount = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )


class MentorInfo(AbstractModel):
    trial_meeting = models.SmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    resume = models.TextField()
    what_help = models.TextField()
    experience = models.TextField()
    portfolio = models.TextField()
    language_set = models.ManyToManyField(Language)
    city = models.TextField()
