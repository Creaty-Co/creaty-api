from __future__ import annotations

from collections.abc import Iterable

from app.base.models.base import BaseModel


class DictManager:
    def __init__(self, objects: Iterable[BaseModel], key: str = 'id'):
        self.objects = {getattr(obj, key): obj for obj in objects}
        self.key = key

    def get(self, **keys: str) -> BaseModel:
        return self.objects[keys[self.key]]
