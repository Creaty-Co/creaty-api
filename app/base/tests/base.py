from typing import Type

from django.db import models
from django.forms import model_to_dict
from rest_framework.test import APIClient, APITestCase

BOUNDARY = "BoUnDaRyStRiNg"
MULTIPART_CONTENT = "multipart/form-data; boundary=%s" % BOUNDARY


class BaseTest(APITestCase):
    client: APIClient

    assert_contains = APITestCase.assertContains
    assert_in = APITestCase.assertIn
    assert_true = APITestCase.assertTrue
    assert_false = APITestCase.assertFalse
    assert_is_instance = APITestCase.assertIsInstance
    assert_is_none = APITestCase.assertIsNone
    assert_is_not_none = APITestCase.assertIsNotNone

    def assert_equal(self, exp_value, value, context=None) -> None:
        match exp_value:
            case dict():
                self.assert_dict(exp_value, value, context=context)
            case list():
                self.assert_list(exp_value, value, context=context)
            case set():
                self.assert_set(exp_value, value, context=context)
            case _:
                if callable(exp_value):
                    if exp_value(value) is False:
                        self.fail(f"{exp_value=}({value=}) is False : {context=}")
                elif exp_value is not ...:
                    self.assert_is_instance(value, type(exp_value), msg=f"{context=}")
                    self.assertEqual(exp_value, value, msg=f"{context=}")

    def assert_list(self, exp_list: list, list_: list, context=None) -> None:
        if exp_list and exp_list[-1] is ...:
            self.assert_list(exp_list[:-1], list_[: len(exp_list) - 1], context=context)
        else:
            self.assert_equal(len(exp_list), len(list_), context=context)
            for exp_element, element in zip(exp_list, list_):
                self.assert_equal(exp_element, element, context=context)

    def assert_set(self, exp_set: set, set_: set, context=None) -> None:
        self.assert_equal(len(exp_set), len(set_), context=context)
        for exp_element in exp_set:
            for element in set_:
                try:
                    self.assert_equal(exp_element, element, context=context)
                    break
                except AssertionError:
                    continue
            else:
                self.fail(f"{exp_set} != {set_} : {context=}")

    def assert_dict(self, exp_dict: dict, dict_: dict, context=None) -> None:
        def dfs(inner_dict, inner_exp_dict):
            def visit(exp_key, exp_value):
                self.assert_in(exp_key, inner_dict)
                value = inner_dict[exp_key]
                if isinstance(value, dict):
                    dfs(value, exp_value)
                else:
                    self.assert_equal(exp_value, value, context=context)

            [visit(*items) for items in inner_exp_dict.items()]

        dfs(dict_, exp_dict)

    def assert_instance(self, instance: models.Model, instance_data: dict):
        instance_dict = model_to_dict(instance)
        self.assert_dict(
            instance_data,
            instance_dict,
            context={
                'instance': instance,
                'instance_data': instance_data,
                'instance_dict': instance_dict,
            },
        )

    def assert_model(
        self,
        model: Type[models.Model] | models.Manager | models.QuerySet | models.Model,
        instance_data: dict,
        **filters,
    ):
        match model:
            case type():  # model is type fo Model
                return self.assert_model(model.objects, instance_data, **filters)
            case models.Manager():
                return self.assert_model(model.all(), instance_data, **filters)
            case models.QuerySet():
                queryset = model
                model = queryset.model
                try:
                    return self.assert_model(
                        queryset.filter(**filters or {}).get(), instance_data
                    )
                except model.DoesNotExist as exc:
                    self.fail(
                        f"{model.__name__} matching query ({filters}) does not exist: "
                        f"({exc})"
                    )
                except model.MultipleObjectsReturned as exc:
                    self.fail(
                        f"{model.__name__} matching query ({filters}) returns "
                        f"multiple objects: ({exc})"
                    )
            case _:  # model is instance
                self.assert_instance(model, instance_data)
        return model
