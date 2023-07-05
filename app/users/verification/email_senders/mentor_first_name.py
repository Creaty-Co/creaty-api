from app.mentors.models import Mentor
from app.users.verification.email_senders.base import BaseEmailSender


class MentorFirstNameEmailSender(BaseEmailSender):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mentor_manager = Mentor.objects

    def _create_context(self, email: str, code, link: str, payload):
        first_name = self.mentor_manager.get(email=email).first_name
        return {'code': code, 'link': link, 'first_name': first_name}
