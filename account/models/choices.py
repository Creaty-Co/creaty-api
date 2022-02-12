from django.db import models


class UserType(models.IntegerChoices):
    ADMIN = 0
    SUPER = 1
