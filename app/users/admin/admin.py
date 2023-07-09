from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app.users.admin.forms import UserChangeForm, UserCreationForm
from app.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'first_name', 'last_name']
    list_filter = []
    fieldsets = [
        (None, {'fields': ['email', 'is_verified', 'has_discount']}),
        ('Personal info', {'fields': ['first_name', 'last_name']}),
        (
            'Permissions',
            {'fields': ['is_staff', 'is_superuser', 'groups', 'user_permissions']},
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['email', 'first_name', 'password1', 'password2'],
            },
        ),
    ]
    search_fields = ['email']
    ordering = None
    filter_horizontal = [
        'groups',
        'user_permissions',
    ]
