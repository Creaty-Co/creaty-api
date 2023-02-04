from typing import Any


class BaseVerifier:
    def send(self, email: str, payload: Any = None) -> None:
        raise NotImplementedError

    def check(self, email: str, code: Any) -> tuple[bool, Any]:
        raise NotImplementedError
