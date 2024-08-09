from datetime import datetime

import pydantic

from app.base.entities.base import BaseEntity
from app.users.models import User


class CalendarEventEntity(BaseEntity):
    start_time: datetime
    end_time: datetime
    title: str
    host: User
    guests: set[User] = pydantic.Field(min_length=1)
