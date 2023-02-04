from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

from django.core.cache import cache

from app.base.exceptions import APIWarning
from app.base.exceptions.base import APIException
from app.base.tests.base import BaseTest
from app.users.models import User
from app.users.tests.factories import UserFactory


class BaseViewTest(BaseTest):
    path: str

    me_class: Callable[..., User] = UserFactory
    me_data: dict[str, Any] | None = {}
    _me = None

    @property
    def me(self) -> User | None:
        if self._me is None:
            if self.me_data is None:
                return None
            self.me = self.me_class(**self.me_data)
        return self._me

    @me.setter
    def me(self, me_):
        del self.me
        self._me = me_
        self.client.force_login(self.me)

    @me.deleter
    def me(self):
        if self._me is not None:
            self.client.logout()
            self._me.delete()
            self._me = None

    def setUp(self):
        cache.clear()
        _ = self.me

    def get(self, path=None, query=None, format=None):
        return self.client.get(
            f'{path or self.path}?{urlencode(query or {})}', format=format
        )

    def post(self, path=None, data=None, format=None):
        return self.client.post(path or self.path, data, format=format)

    def put(self, path=None, data=None, format=None):
        return self.client.put(path or self.path, data, format=format)

    def patch(self, path=None, data=None, format=None):
        return self.client.patch(path or self.path, data, format=format)

    def delete(self, path=None, data=None, format=None):
        return self.client.delete(path or self.path, data, format=format)

    def assert_response(self, response, status=200, data: dict = None):
        self.assert_equal(response.status_code, status)
        self.assert_json(response.json() if response.content else {}, data or {})

    def _test(
        self,
        method: str,
        exp_data: dict[str, Any] | APIException = None,
        data: dict[str, Any] = None,
        status: int = None,
        path: str = None,
        format=None,
    ):
        response = getattr(self, method)(path, data, format)
        if response.content:
            status = status or {'post': 201, 'delete': 204}.get(method, 200)
        else:
            status = 204
        if isinstance(exp_data, APIException):
            status = exp_data.status
            exp_exception = {'error': {'type': exp_data.TYPE_NAME}}
            if isinstance(exp_data, APIWarning):
                exp_exception['error']['code'] = exp_data.code
            exp_data = exp_exception
        self.assert_response(response, status, exp_data)
