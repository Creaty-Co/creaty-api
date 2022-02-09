from base.views.base import BaseView
from forms.services.applications_xlsx import ApplicationsXlsxConverter


# noinspection PyMethodMayBeStatic
class FormsApplicationsXlsxView(BaseView):
    def get(self, request):
        return ApplicationsXlsxConverter().to_response()
