from app.users.models import User


def user_details(strategy, details, backend, user=None, *_, **__):
    if not user:
        return
    changed = False
    private = {'id', 'pk', 'password', 'is_staff', 'is_superuser'}
    if strategy.setting('NO_DEFAULT_PROTECTED_USER_FIELDS') is True:
        protected = set()
    else:
        protected = {'username', 'email'}
    protected = set(
        list(protected) + list(strategy.setting('PROTECTED_USER_FIELDS', []))
    )
    for protected_field in protected.copy():
        if protected_field == User.USERNAME_FIELD:
            protected.remove(protected_field)
            private.add(protected_field)

    field_mapping = strategy.setting('USER_FIELD_MAPPING', {}, backend)
    for name, value in details.items():
        name = field_mapping.get(name, name)
        if not hasattr(user, name) or name in private:
            continue
        try:
            current_value = getattr(user, name)
        except AttributeError:
            continue
        if current_value == value:
            continue
        if name not in protected or not current_value:
            changed = True
            setattr(user, name, value)
    if changed:
        strategy.storage.user.changed(user)
