from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, TypeAlias

from app.base.entities.base import BaseEntity
from app.base.models.base import BaseModel

_EntityType: TypeAlias = Type[BaseEntity] | Type[BaseModel]


class BaseAction(ABC):
    InEntity: type[_EntityType] = None
    OutEntity: type[_EntityType] = None

    @abstractmethod
    def run(self, data: InEntity) -> OutEntity:
        raise NotImplementedError
