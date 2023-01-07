from app.base.views.xlsx import BaseXlsxView
from app.forms.services.applications_xlsx import ApplicationsXlsxConverter


class FormsApplicationsXlsxView(BaseXlsxView):
    xlsx_converter = ApplicationsXlsxConverter()
