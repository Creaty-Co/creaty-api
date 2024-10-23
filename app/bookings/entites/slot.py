from datetime import datetime

from app.base.entities.base import BaseEntity


class SlotEntity(BaseEntity):
    start_time: datetime
    end_time: datetime
    is_free: bool
