from cacheops import invalidate_obj
from django.conf import settings
from django.contrib.auth.hashers import is_password_usable
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from uuslug import uuslug

from app.base.models.base import BaseModel
from app.base.money import Money
from app.geo.models import *
from app.tags.models import Tag
from app.users.models import User

__all__ = ['Mentor', 'Package']


class Mentor(User):
    user_ptr: User
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(Tag, related_name='mentors')
    languages = models.ManyToManyField(Language, related_name='mentors')
    country = models.ForeignKey(Country, models.PROTECT, related_name='mentors')
    company = models.TextField(blank=True, default='')
    profession = models.TextField()
    price: Money = MoneyField(max_digits=10, decimal_places=2)
    is_draft = models.BooleanField(default=True)
    trial_meeting = models.SmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    resume = models.TextField()
    what_help = models.TextField(blank=True, default='')
    experience = models.TextField(blank=True, default='')
    city = models.TextField(blank=True, default='')
    links = ArrayField(models.URLField(), blank=True, default=list)

    @property
    def url(self) -> str:
        return f"https://{settings.WEB_DOMAIN}/mentor/{self.slug}"

    @property
    def is_registered(self) -> bool:
        return is_password_usable(self.password) or self.social_auth.exists()

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuslug(f"{self.first_name}_{self.last_name}", self)
        super().save(**kwargs)
        invalidate_obj(self.user_ptr)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Package(BaseModel):
    mentor = models.ForeignKey(Mentor, models.CASCADE, related_name='packages')
    lessons_count = models.SmallIntegerField(validators=[MinValueValidator(2)])
    discount = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )

    def __str__(self):
        return f"{self.mentor}: {self.lessons_count} → {self.discount}%"
