from __future__ import annotations

import datetime
from collections.abc import Callable, Sequence
from typing import Any, Final

from django.core.files.base import ContentFile
from factory import Faker as _FactoryFaker
from faker import Faker as _Faker
from faker import Generator


class SubFaker(_Faker):
    first_name: Callable[..., str]
    last_name: Callable[..., str]
    password: Callable[..., str]
    email: Callable[..., str]
    future_date: Callable[..., datetime.date]
    random_element: Callable

    def __init__(
        self,
        locale: None | (str | Sequence[str] | dict[str, int | float]) = 'en_PH',
        providers: list[str] | None = None,
        generator: Generator | None = None,
        includes: list[str] | None = None,
        use_weighting: bool = True,
        **config: Any,
    ) -> None:
        super().__init__(
            locale, providers, generator, includes, use_weighting, **config
        )

    def random_string(self, length: int = 10):
        letters_count = self.random_int(max=length)
        letters = self.random_letters(letters_count)
        numbers = [str(self.random_digit()) for _ in range(length - letters_count)]
        return ''.join(self.random_elements(letters + numbers, length, True))

    def image(self, size: tuple[int, int] = (1, 1), extension=None) -> ContentFile:
        if extension is None:
            extension = self.file_extension(category='image')
        extension = 'jpeg' if extension == 'jpg' else extension
        return ContentFile(
            self.__getattr__('image')(size=size, image_format=extension),
            fake.file_name(category='image', extension=extension),
        )


class Faker(_FactoryFaker):
    def __init__(self, provider, **kwargs):
        kwargs.setdefault('locale', 'en_PH')
        super().__init__(provider, **kwargs)

    @classmethod
    def _get_faker(cls, locale='en_PH'):
        if locale not in cls._FAKER_REGISTRY:
            sub_faker = fake.unique
            cls._FAKER_REGISTRY[locale] = sub_faker
        return cls._FAKER_REGISTRY[locale]


fake: Final[SubFaker] = SubFaker()
