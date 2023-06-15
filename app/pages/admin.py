from django import forms
from django.contrib import admin

from ..mentors.models import Mentor
from .models import Page, PageMentors


class PageMentorsInline(admin.TabularInline):
    model = PageMentors
    extra = 1
    ordering = ['index']


class MentorCheckboxWidget(forms.CheckboxSelectMultiple):
    template_name = 'mentor_checkbox_widget.html'

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        option['index'] = index
        return option


class PageForm(forms.ModelForm):
    mentors = forms.ModelMultipleChoiceField(
        queryset=Mentor.objects.all(),
        widget=MentorCheckboxWidget,
        required=False,
    )

    class Meta:
        model = Page
        fields = '__all__'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    inlines = [PageMentorsInline]
    list_display = ['__str__']
    list_filter = [
        'tag',
        'category',
    ]
    search_fields = [
        'tag__name',
        'category__name',
    ]
    filter_horizontal = ['tags']
