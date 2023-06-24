from app.users.verification.link_generators.email.base import BaseLinkGenerator


class CodeLinkGenerator(BaseLinkGenerator):
    def generate(self, code, email: str, payload=None) -> str:
        return self._generate(code)
