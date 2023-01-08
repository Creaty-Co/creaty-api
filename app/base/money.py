from django.conf import settings
from djmoney import money, serializers, utils
from djmoney.contrib.django_rest_framework import fields as django_rest_framework_fields
from djmoney.contrib.exchange.models import convert_money
from djmoney.forms import fields as forms_fields
from djmoney.models import fields as models_fields


class Money(money.Money):
    def __init__(self, *args, **kwargs):
        if len(args) <= 1:
            kwargs.setdefault('currency', settings.DEFAULT_CURRENCY)
        super().__init__(*args, **kwargs)

    def convert(self, currency: str = None):
        currency = currency or settings.DEFAULT_CURRENCY
        return convert_money(self, currency)


money.Money = Money
serializers.Money = Money
utils.MONEY_CLASSES = (Money, utils.MONEY_CLASSES[1])
forms_fields.Money = Money
models_fields.Money = Money
django_rest_framework_fields.Money = Money
