from base.views.xlsx import BaseXlsxView
from forms.services.applications_xlsx import ApplicationsXlsxConverter


# noinspection PyMethodMayBeStatic
class FormsApplicationsXlsxView(BaseXlsxView):
    xlsx_converter = ApplicationsXlsxConverter()
