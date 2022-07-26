from django.conf import settings
from django.shortcuts import redirect

from base.logs import warning
from base.utils.decorators import schema_redirect
from base.views.base import BaseView
from mailings.models import Subscriber


class MailingsUnsubscribeView(BaseView):
    queryset = Subscriber.objects.all()
    lookup_field = 'uuid'

    @schema_redirect(f'redirect: {settings.REDIRECT_ON_UNSUBSCRIBE}')
    def get(self, request, **_):
        try:
            subscriber = self.get_object()
            subscriber.delete()
        except Exception as e:
            warning(str(e))
        return redirect(settings.REDIRECT_ON_UNSUBSCRIBE)
