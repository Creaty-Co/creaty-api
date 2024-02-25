from app.base.models.base import BaseModel
from app.cal.managers import CalManager


class BaseCalModel(BaseModel):
    objects = CalManager()

    class Meta:
        abstract = True
        managed = False
