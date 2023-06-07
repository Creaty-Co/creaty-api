from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app.users.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'first_name']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'style': 'height: 15px; width: 200px'}
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={'style': 'height: 15px; width: 200px'}
            ),
            'last_name': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['id', 'email', 'first_name', 'last_name']
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
