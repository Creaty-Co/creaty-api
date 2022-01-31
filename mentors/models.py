from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from base.models import AbstractModel


class Mentor(AbstractModel):
    info = models.OneToOneField('MentorInfo', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    company = models.TextField(null=True, blank=True)
    profession = models.TextField(null=True, blank=True)
    first_name = models.TextField()
    last_name = models.TextField()
    # tag_set  TODO: #24
    # price  TODO: #24


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
