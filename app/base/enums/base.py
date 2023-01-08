from __future__ import annotations

from enum import EnumMeta, unique

from django.db.models import IntegerChoices as _IntegerChoices
from django.db.models import TextChoices as _TextChoices
from django.db.models import enums
from django.utils.functional import Promise

ChoicesMeta = getattr(enums, 'ChoicesMeta')

__all__ = ['BaseEnumStr', 'BaseEnumInt']


class _BaseEnumMeta(ChoicesMeta):
    def __new__(cls, classname, bases, class_dict, **kwargs):
        labels = []
        for index, key in enumerate(getattr(class_dict, '_member_names')):
            value, label = cls._parse(index, key, class_dict[key])
            labels.append(label)
            dict.__setitem__(class_dict, key, value)
        self: _BaseEnumMeta = EnumMeta.__new__(
            cls, classname, bases, class_dict, **kwargs
        )
        self.dict_by_value = self._value2label_map_ = dict(
            zip(self._value2member_map_, labels)
        )
        self.dict_by_name = self._member_map_
        self.label = property(lambda self_: self._value2label_map_.get(self_.value))
        self.help_text = self.__help_text()
        # noinspection PyTypeChecker
        return unique(self)

    @classmethod
    def _parse(cls, index, key, value):
        raise NotImplementedError

    def __help_text(self) -> str:
        self: ChoicesMeta
        transcripts = []
        for member in self:
            if member.name == member.label:
                transcripts.append(f'{member.value} — {member.label}')
            else:
                transcripts.append(f'{member.value} — {member.name} ({member.label})')
        return '\n\n'.join(transcripts)


class _TextEnumMeta(_BaseEnumMeta):
    @classmethod
    def _parse(cls, index, key, value):
        if isinstance(value, (list, tuple)):
            if len(value) > 1 and isinstance(value[-1], (Promise, str)):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace('_', ' ').capitalize()
        elif value is ...:
            label = key.replace('_', ' ').capitalize()
            value = key.upper()
        else:
            label = value
            value = key.upper()
        return value, label


class BaseEnumStr(_TextChoices, metaclass=_TextEnumMeta):
    help_text: str
    dict_by_name: dict[str, BaseEnumStr]
    dict_by_value: dict[str, BaseEnumStr]


class _IntegerEnumMeta(_BaseEnumMeta):
    @classmethod
    def _parse(cls, index, key, value):
        if isinstance(value, (list, tuple)):
            if len(value) > 1 and isinstance(value[-1], (Promise, str)):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace('_', ' ').capitalize()
        elif value is ...:
            label = key.replace('_', ' ').capitalize()
            value = index
        else:
            label = value
            value = index
        return value, label


class BaseEnumInt(_IntegerChoices, metaclass=_IntegerEnumMeta):
    help_text: str
    dict_by_name: dict[str, BaseEnumInt]
    dict_by_value: dict[int, BaseEnumInt]


BaseEnumStr: type[_TextChoices | BaseEnumStr | str]
BaseEnumInt: type[_IntegerChoices | BaseEnumInt | int]
