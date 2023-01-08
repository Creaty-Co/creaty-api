from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.context import make_context
from django.utils.functional import cached_property
from templated_mail.mail import BaseEmailMessage


class MailingEmailMessage(BaseEmailMessage):
    BASE_TEMPLATE_PATH = 'mailings/templates/base.html'

    def __init__(self, mailing, subscriber, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailing = mailing
        self.to = [subscriber.email]
        self.context.setdefault('subscriber', subscriber)
        self.context.setdefault('mailing', self.mailing)

    @cached_property
    def _template_content(self) -> str:
        with open(self.BASE_TEMPLATE_PATH) as base_html:
            return base_html.read()

    @property
    def _template(self) -> Template:
        content = self._template_content.replace('__content__', self.mailing.content)
        return Template(content)

    def render(self):
        context = make_context(self.get_context_data(), request=self.request)
        template = self._template
        with context.bind_template(template):
            for node in template.nodelist:
                self._process_node(node, context)
        self._attach_body()

    def send(self, **_):
        self.render()
        EmailMultiAlternatives.send(self)
