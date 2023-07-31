from rest_framework.generics import get_object_or_404

from app.admin_.services.notification import AdminNotificationService
from app.base.notificators.emails.base import BaseEmailNotifier
from app.base.services.email.senders.base import BaseEmailSender
from app.base.utils.common import response_204
from app.base.views.base import BaseView
from app.forms.models import Form
from app.forms.models.choices import FormType
from app.forms.serializers.applications.general import FormApplicationsSerializer
from app.users.models import User


class FormApplicationsView(BaseView):
    serializer_map = {'post': FormApplicationsSerializer}

    @response_204
    def post(self):
        form = get_object_or_404(Form, id=self.kwargs['form_id'])
        serializer = self.get_valid_serializer()
        application = serializer.save(form=form)
        AdminNotificationService().on_application(application)
        if (
            form.type == FormType.BECOME_MENTOR
            or not User.objects.filter(email=application.email).exists()
        ):
            match form.type:
                case FormType.BECOME_MENTOR:
                    template_name = 'email/mentors-application.html'
                case FormType.CHOOSE_MENTOR:
                    template_name = 'email/find-mentor.html'
                case FormType.TEST_MEETING:
                    template_name = 'email/first-trial-session.html'
                case _:
                    return
            user_notifier = BaseEmailNotifier(
                email_sender=BaseEmailSender(template_name=template_name)
            )
            user_notifier.notify(
                [
                    user_notifier.Notification(
                        email=application.email, context={'application': application}
                    )
                ]
            )
