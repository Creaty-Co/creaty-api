from django.http import QueryDict

from app.base.tests.admin.base import BaseAdminTest
from app.base.tests.fakers import fake
from app.tags.admin import TagAdminForm
from app.tags.models import Tag
from app.tags.tests.factories import CategoryFactory


class TestTagAdmin(BaseAdminTest):
    def test_add(self):
        data = QueryDict(mutable=True)
        data.update(
            {
                'title': fake.english_word(),
                'shortcut': fake.english_word(),
                'categories': CategoryFactory().id,
            }
        )
        form = TagAdminForm(data=data)
        self.assert_true(form.is_valid(), form.errors)
        form.save()
        self.assert_model(Tag, {})
