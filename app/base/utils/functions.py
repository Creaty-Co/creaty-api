from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeVar

from django.db import models
from django.db.models import Choices

__all__ = [
    'status_by_method',
    'choices_to_help_text',
    'reverse_choices',
    'choices_to_dict',
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
    choices: type[models.Choices] | Iterable[tuple[Any, str]]
) -> str:
    transcripts = []
    if isinstance(choices, type) and issubclass(choices, Choices):
        for member in choices:
            transcripts.append(f'{member.value} — {member.name} ({member.label})')
    else:
        choices: Iterable
        for member in choices:
            transcripts.append(f'{member[0]} — {member[1]}')
    return '\n\n'.join(transcripts)


def reverse_choices(choices: type[_Choices]) -> dict[Any, _Choices]:
    return {member.value: member for member in choices}


def choices_to_dict(choices: type[_Choices]) -> dict[Any, _Choices]:
    return {member.name: member for member in choices}
