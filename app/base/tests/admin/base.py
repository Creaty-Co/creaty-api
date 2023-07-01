from django.test import override_settings

from app.base.tests.views.base import BaseViewTest


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class BaseAdminTest(BaseViewTest):
    me_data = {'is_staff': True, 'is_superuser': True}
