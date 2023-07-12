from app.users.notificators.email import UsersEmailNotifier


class OperatorsEmailNotifier(UsersEmailNotifier):
    GROUP_NAME = 'operator'

    @property
    def default_users(self):
        return self.user_manager.filter(groups__name=self.GROUP_NAME)
