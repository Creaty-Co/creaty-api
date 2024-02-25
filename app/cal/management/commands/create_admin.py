from django.core.management.base import BaseCommand

from app.cal.models import CalUser
from app.cal.services.auth import CalAuthService
from app.users.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = User.objects
        self.cal_user_manager = CalUser.objects
        self.cal_auth_service = CalAuthService()

    def handle(self, id, **options):
        user_admin = self.user_manager.get(id=id)
        self.cal_auth_service.register(user_admin)
        token = self.cal_auth_service.token(user_admin)
        self.stdout.write(f"Cal admin token: {token}")

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='User id')
