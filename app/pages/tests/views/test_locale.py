from app.base.tests.views.base import BaseViewTest


class PagesLocalesLanguageTranslationJsonTest(BaseViewTest):
    path = '/pages/locales/en/translation.json/'

    def test_put_success(self):
        self._test('put', data={'language': 'en'})
