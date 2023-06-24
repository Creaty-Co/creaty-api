from app.mentors.models import Mentor
from app.users.verification.link_generators.email.base import BaseLinkGenerator


class MentorLinkGenerator(BaseLinkGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mentor_manager = Mentor.objects

    def generate(self, code, email: str, payload=None) -> str:
        """
        :raises Mentor.DoesNotExist: if mentor with email doesn't exists
        """
        first_name = self.mentor_manager.get(email=email).first_name
        return self._generate(code, first_name=first_name)
