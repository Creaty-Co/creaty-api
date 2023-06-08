from django.core.management.base import BaseCommand

from app.users.models import User


class Command(BaseCommand):
    ADMIN_EMAIL = 'admin@mail.com'
    ADMIN_PASSWORD = 'c00lPass'
    ADMIN_FIRST_NAME = 'admin'

    def handle(self, *args, **options):
        User.objects.create_user(
            email=self.ADMIN_EMAIL,
            password=self.ADMIN_PASSWORD,
            first_name=self.ADMIN_FIRST_NAME,
            is_verified=True,
            has_discount=True,
            is_staff=True,
            is_superuser=True,
        )
