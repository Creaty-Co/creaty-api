from django.conf import settings
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money as _Money
from djmoney.models import fields


class Money(_Money):
    def __init__(self, *args, **kwargs):
        if len(args) <= 1:
            kwargs.setdefault('currency', settings.DEFAULT_CURRENCY)
        super().__init__(*args, **kwargs)

    def convert(self, currency: str = settings.DEFAULT_CURRENCY):
        return convert_money(self, currency)


fields.Money = Money
