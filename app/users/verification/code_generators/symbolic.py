from django.utils.crypto import get_random_string

from app.users.verification.code_generators.base import BaseCodeGenerator


class SymbolicCodeGenerator(BaseCodeGenerator):
    def __init__(self, length: int):
        self.length = length

    def generate(self) -> int:
        return get_random_string(self.length)

    def is_equal(self, code1, code2) -> bool:
        return str(code1) == str(code2)
