from app.base.filtersets.base import BaseFilterSet
from app.forms.models import Form


class FormsFilterSet(BaseFilterSet):
    class Meta:
        model = Form
        fields = {'type': ['in']}
