from django.http import HttpResponseRedirect
from drf_spectacular.utils import OpenApiResponse

from app.base.utils.schema import extend_schema
from app.base.views import BaseView
from app.users.regisration import registerer


class UsersRegisterCodeView(BaseView):
    @extend_schema(
        responses={
            200: None,
            302: OpenApiResponse(
                description=(
                    f"redirect:"
                    f"\n\n{'&nbsp;' * 4}failure url: {registerer.failure_url}"
                    f"\n\n{'&nbsp;' * 4}successful url: {registerer.successful_url}"
                )
            ),
        }
    )
    def get(self):
        code = self.kwargs['code']
        if registerer.register(code):
            return HttpResponseRedirect(registerer.successful_url)
        return HttpResponseRedirect(registerer.failure_url)
