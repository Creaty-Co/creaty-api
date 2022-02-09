from typing import Iterable

from django.db.models import F

from base.services.xlsx import XlsxConverter
from base.utils.functions import reverse_choices
from forms.models import Application
from forms.models.choices import FormField, FormType


class ApplicationsXlsxConverter(XlsxConverter):
    MODEL = Application
    # noinspection PyUnresolvedReferences
    FIELD_HEADER_MAP = {'type': 'Тип', 'id': 'Id'} | {_.value: _.label for _ in FormField}
    
    def __init__(self):
        super().__init__(self.FIELD_HEADER_MAP)
    
    def _get_values(self) -> Iterable:
        values = list(
            self.MODEL.objects.annotate(type=F('form__type')).order_by(
                'type', 'id'
            ).values_list(*self.fields)
        )
        for i in range(len(values)):
            values[i] = (reverse_choices(FormType)['become_mentor'].label, *values[i][1:])
        return values
