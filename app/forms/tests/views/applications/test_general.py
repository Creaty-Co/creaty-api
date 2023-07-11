from django.core import mail
from parameterized import parameterized

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.forms.models import Application, Form
from app.forms.models.choices import FormType
from app.forms.tests.factories import FormFactory
from app.users.tests.factories import GroupFactory, UserFactory


class FormsApplicationsTest(BaseViewTest):
    form: Form

    @property
    def path(self):
        return f"/forms/{self.form.id}/applications/"

    @parameterized.expand(
        [(choice, choice != FormType.STILL_QUESTIONS) for choice in FormType]
    )
    def test_post(self, form_type: FormType, expects_emails: bool):
        self.form = FormFactory(type=form_type)
        operator = UserFactory()
        operator.groups.add(GroupFactory(name='operator'))
        email = fake.email()
        data = {
            'path': '/' + fake.uri_path(),
            'name': fake.first_name(),
            'email': email,
            'about': fake.text(),
            'link': fake.url(),
        }
        self._test('post', data=data)
        self.assert_model(Application, {'form': self.form.id, **data})
        if expects_emails:
            self.assert_equal(
                {
                    lambda message: self.assert_equal(message.to, [email]),
                    lambda message: self.assert_equal(message.to, [operator.email]),
                },
                set(mail.outbox),
            )
        else:
            self.assert_equal(0, len(mail.outbox))
