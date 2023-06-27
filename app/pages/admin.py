from django import forms
from django.contrib import admin
from django.db import transaction
from django.db.models import Q

from app.mentors.models import Mentor
from app.pages.models import Page, PageMentors
from app.tags.admin import MentorCheckboxSelectMultiple, MultipleChoiceField


class PageAdminForm(forms.ModelForm):
    mentors_on_page = MultipleChoiceField(
        widget=MentorCheckboxSelectMultiple(), required=False
    )

    class Meta:
        model = Page
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        page = self.instance
        choices = []
        mentors = Mentor.objects.distinct()
        if page.tag:
            mentors = mentors.filter(Q(tags=page.tag) | Q(pages=page))
        elif page.category:
            mentors = mentors.filter(Q(tags__categories=page.category) | Q(pages=page))
        for mentor in mentors:
            page_mentors = PageMentors.objects.filter(page=page, mentor=mentor).first()
            mentor.index = page_mentors.index if page_mentors else -1
            choices.append((mentor, str(mentor)))
        self.fields['mentors_on_page'].choices = choices

    @transaction.atomic
    def save(self, commit=True):
        mentors = self.cleaned_data['mentors_on_page']
        page = super().save(commit=False)
        if commit:
            page.save()
        if page is not None:
            page.page_mentors.all().delete()
            for mentor in mentors:
                PageMentors.objects.create(page=page, mentor=mentor, index=mentor.index)
        return page


class PageMentorsInline(admin.TabularInline):
    model = PageMentors
    extra = 1
    ordering = ['index']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    # inlines = [PageMentorsInline]
    # fields = ['tag', 'category', 'tags', 'mentors_on_page']
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
