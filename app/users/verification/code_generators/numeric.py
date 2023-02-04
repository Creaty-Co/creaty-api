import random

from app.users.verification.code_generators.base import BaseCodeGenerator


class NumericCodeGenerator(BaseCodeGenerator):
    def __init__(self, min_: int, max_: int):
        self.min = min_
        self.max = max_

    def generate(self) -> int:
        return random.randint(self.min, self.max)

    def is_equal(self, code1, code2) -> bool:
        try:
            return int(code1) == int(code2)
        except (ValueError, TypeError):
            return False
