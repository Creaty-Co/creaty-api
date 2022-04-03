from django.db.models import F

from base.services.xlsx import BaseXlsxConverter
from forms.models import Application, Form
from forms.models.choices import FormField, FormType, rFormType

_FormTypeByLabel = {_.label: _ for _ in FormType}


class ApplicationsXlsxConverter(BaseXlsxConverter):
    MODEL = Application
    FIELD_HEADER_MAP = {'type': 'Тип', 'id': 'Id', 'URL': 'url'} | {
        _.value: _.label for _ in FormField
    }
    
    def __init__(self):
        super().__init__(self.FIELD_HEADER_MAP)
    
    def _get_values(self):
        values = list(
            self.MODEL.objects.annotate(type=F('form__type')).order_by(
                'type', 'id'
            ).values_list(*self.fields)
        )
        for i, value in enumerate(values):
            values[i] = (rFormType[value[0]].label, *value[1:])
        return values
    
    def _update_objects(self, instances_data):
        for instance_data in instances_data.values():
            instance_data['form'] = Form.objects.get(
                type=_FormTypeByLabel[instance_data.pop(self._header_by_field('type'))]
            )
        super()._update_objects(instances_data)
