from app.users.notificators.email import UsersEmailNotifier


class StaffEmailNotifier(UsersEmailNotifier):
    @property
    def default_users(self):
        return self.user_manager.filter(is_staff=True)
