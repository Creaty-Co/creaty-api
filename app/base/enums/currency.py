from __future__ import annotations

from collections.abc import Iterable

import moneyed
from moneyed import CurrencyDoesNotExist, get_currency

from app.base.enums.base import BaseEnumStr


class Currency(BaseEnumStr):
    RUB = 'Рубль (₽)'
    USD = 'Доллар США ($)'
    EUR = 'Евро (€)'


Currency: Iterable


for _currency in tuple(Currency):
    try:
        get_currency(_currency)
    except CurrencyDoesNotExist:
        moneyed.add_currency(code=_currency, numeric=None, name=_currency.label)
