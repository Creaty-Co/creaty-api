from abc import ABC, abstractmethod
from typing import Type, TypeAlias

from app.base.entities.base import BaseEntity
from app.base.models.base import BaseModel

_EntityType: TypeAlias = Type[BaseEntity] | Type[BaseModel]


class BaseChecker(ABC):
    InEntity: _EntityType = None

    @abstractmethod
    def check(self, data: 'InEntity') -> bool:
        raise NotImplementedError
