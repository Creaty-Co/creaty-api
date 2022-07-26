import re

from django.db.models import F

from base.services.xlsx import BaseXlsxConverter
from forms.models import Application, Form
from forms.models.choices import FormField, FormType, rFormType
from mentors.models import Mentor

_FormTypeByLabel = {_.label: _ for _ in FormType}


class ApplicationsXlsxConverter(BaseXlsxConverter):
    MODEL = Application
    FIELD_HEADER_MAP = (
        {'type': 'Тип', 'id': 'Id', 'path': 'Path'}
        | {_.value: _.label for _ in FormField}
        | {'mentor_fullname': 'Имя ментора'}
    )

    def __init__(self):
        super().__init__(self.FIELD_HEADER_MAP)

    def _get_values(self):
        values = list(
            self.MODEL.objects.annotate(type=F('form__type'))
            .order_by('type', 'id')
            .values_list(*self.fields[:-1])
        )
        for i, value in enumerate(values):
            application_type = rFormType[value[0]]
            mentor_fullname = ''
            if match := re.match(r'/user/(\d+).*', value[2]):
                if mentor := Mentor.objects.filter(id=match.group(1)).first():
                    mentor_fullname = f'{mentor.first_name_en} {mentor.last_name_en}'
            values[i] = (application_type.label, *value[1:], mentor_fullname)
        return values

    def _update_objects(self, instances_data):
        for instance_data in instances_data.values():
            instance_data['form'] = Form.objects.get(
                type=_FormTypeByLabel[instance_data.pop(self._header_by_field('type'))]
            )
        super()._update_objects(instances_data)
