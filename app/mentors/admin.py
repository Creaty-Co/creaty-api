from django import forms
from django.contrib import admin
from django.utils.html import format_html

from app.mentors.models import Mentor, Package
from app.pages.models import PageMentors
from app.users.models import User
from app.users.password_reset import password_resetter


class PackageInline(admin.TabularInline):
    model = Package
    extra = 1


class PageInline(admin.TabularInline):
    model = PageMentors
    raw_id_fields = ['page']
    extra = 1


class MentorAdminForm(forms.ModelForm):
    instance: User

    class Meta:
        model = Mentor
        fields = '__all__'
        widgets = {
            'slug': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'company': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'first_name': forms.TextInput(
                attrs={'style': 'height: 15px; width: 200px'}
            ),
            'last_name': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'city': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_m2m = None
        self.fields['what_help'].label = "How can I help"
        self.fields['slug'].required = False

    def save(self, commit=True):
        self.instance.is_verified = True
        self.instance.has_discount = True
        if not self.instance.id:
            self.instance.set_password(None)
        super().save(commit)
        return self.instance


def send_password_reset_email(_, __, queryset):
    for mentor in queryset:
        password_resetter.send_to_user(mentor.email)


def send_mentor_registration_email(_, __, queryset):
    for mentor in queryset:
        password_resetter.send_to_mentor(mentor.email)


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    form = MentorAdminForm
    list_display = ['__str__', 'url', 'is_draft', 'is_registered']
    list_display_links = ['__str__']
    list_editable = ['is_draft']
    list_filter = ['is_draft']
    fieldsets = (
        (
            "Profile Information",
            {
                'fields': [
                    'is_draft',
                    'slug',
                    'link',
                    'avatar_image',
                    'avatar',
                    'first_name',
                    'last_name',
                    'email',
                    'country',
                    'city',
                ]
            },
        ),
        (
            "Professional Details",
            {
                'fields': [
                    'languages',
                    'tags',
                    'resume',
                    'experience',
                    'what_help',
                    'profession',
                    'company',
                    'price',
                    'trial_meeting',
                ]
            },
        ),
    )
    filter_vertical = ['tags', 'languages']
    readonly_fields = ['avatar_image', 'url']
    search_fields = ['first_name', 'last_name']
    actions = [send_password_reset_email, send_mentor_registration_email]
    inlines = [PackageInline, PageInline]

    def avatar_image(self, obj):
        return format_html('<img src="{}" width="500"/>', obj.avatar.url)

    def url(self, obj):
        return format_html('<a href="{}">{}</a>', obj.url, obj.url)

    def is_registered(self, obj: Mentor) -> bool:
        return obj.is_registered

    is_registered.boolean = True

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
