from typing import Any, Iterable, Type, TypeVar
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.db import models
from django.db.models import Choices
from rest_framework import serializers

__all__ = [
    'status_by_method', 'choices_to_help_text', 'add_query_params', 'schema_serializer',
    'reverse_choices', 'choices_to_dict'
]

_Choices = TypeVar('_Choices', bound=models.Choices)


def status_by_method(method: str) -> int:
    match method.lower():
        case 'post':
            return 201
        case 'delete':
            return 204
        case _:
            return 200


def choices_to_help_text(
    choices: Type[models.Choices] | Iterable[tuple[Any, str]]
) -> str:
    transcripts = []
    if isinstance(choices, type) and issubclass(choices, Choices):
        for member in choices:
            transcripts.append(f'{member.value} — {member.name} ({member.label})')
    else:
        for member in choices:
            transcripts.append(f'{member[0]} — {member[1]}')
    return '\n\n'.join(transcripts)


def reverse_choices(choices: Type[_Choices]) -> dict[Any, _Choices]:
    return {member.value: member for member in choices}


def choices_to_dict(choices: Type[_Choices]) -> dict[Any, _Choices]:
    return {member.name: member for member in choices}


def add_query_params(url: str, **query_params: Any) -> str:
    url_parts = list(urlparse(url))
    old_query_params = dict(parse_qsl(url_parts[4]))
    new_query_params = {k: str(v) for k, v in query_params.items()}
    url_parts[4] = urlencode(old_query_params | new_query_params)
    return urlunparse(url_parts)


def schema_serializer(
    _name: str, **fields: serializers.Field
) -> Type[serializers.Serializer]:
    if not _name.endswith('Serializer'):
        _name += 'Serializer'
    # noinspection PyTypeChecker
    return type(_name, (serializers.Serializer,), fields)
