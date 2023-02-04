from typing import Any


class BaseCodeGenerator:
    def generate(self) -> Any:
        raise NotImplementedError

    def is_equal(self, code1, code2) -> bool:
        return code1 == code2
