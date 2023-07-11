from app.users.notificators.email import UsersEmailNotifier


class StaffEmailNotifier(UsersEmailNotifier):
    @property
    def users(self):
        return self.user_manager.filter(is_staff=True)
