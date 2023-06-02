from django import forms
from django.contrib import admin
from django.core.validators import MinValueValidator

from .models import Mentor, MentorInfo, Package


class PackageInline(admin.TabularInline):
    model = Package
    extra = 1


class MentorAdminForm(forms.ModelForm):
    trial_meeting = forms.IntegerField(
        required=False, validators=[MinValueValidator(1)]
    )
    resume = forms.CharField(widget=forms.Textarea)
    what_help = forms.CharField(required=False, widget=forms.Textarea)
    experience = forms.CharField(required=False, widget=forms.Textarea)
    city = forms.CharField(required=False)

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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            mentor_info = self.instance.info
            self.fields['trial_meeting'].initial = mentor_info.trial_meeting
            self.fields['resume'].initial = mentor_info.resume
            self.fields['what_help'].initial = mentor_info.what_help
            self.fields['experience'].initial = mentor_info.experience
            self.fields['city'].initial = mentor_info.city


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    form = MentorAdminForm
    list_display_links = ['id', 'first_name']
    list_display = ['id', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'profession', 'company']
    inlines = [PackageInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        data = form.cleaned_data
        MentorInfo.objects.update_or_create(
            mentor=obj,
            defaults={
                'trial_meeting': data.get('trial_meeting'),
                'resume': data.get('resume'),
                'what_help': data.get('what_help'),
                'experience': data.get('experience'),
                'city': data.get('city'),
            },
        )
