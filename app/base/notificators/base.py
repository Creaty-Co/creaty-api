from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.base.entities.base import BaseEntity


class BaseNotifier(ABC):
    class Notification(BaseEntity):
        pass

    @abstractmethod
    def notify(self, notifications: Iterable[Notification]) -> None:
        raise NotImplementedError
