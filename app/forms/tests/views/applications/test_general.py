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
    def test_post(self, form_type: FormType, is_expects_emails: bool):
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
        expected_emails = {
            lambda message: self.assert_equal(message.to, [operator.email])
        }
        if is_expects_emails:
            expected_emails.add(lambda message: self.assert_equal(message.to, [email]))
        self.assert_equal(expected_emails, set(mail.outbox))
