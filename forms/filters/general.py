from base.filters.base import BaseFilterSet
from forms.models import Form


class FormsFilterSet(BaseFilterSet):
    class Meta:
        model = Form
        fields = {'type': ['in']}
