from abc import ABC

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import transaction
from django.db.models import Q
from django.utils.html import format_html

from app.base.forms.fields.image import ImageFormField
from app.mentors.models import Mentor
from app.pages.models import PageMentors
from app.tags.models import Category, CategoryTag, Tag


class MentorCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'mentor_checkbox_widget.html'

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        selected = value.index != -1
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        option['page_index'] = value.index
        return option

    def value_from_datadict(self, data, files, name):
        mentors_map = {mentor_label: mentor for mentor, mentor_label in self.choices}
        selected_mentor_labels = data.getlist(name)
        mentors_data = []
        for selected_mentor_label in selected_mentor_labels:
            mentor = mentors_map[selected_mentor_label]
            mentor.index = data.get(f"page_index_{mentor.id}")
            mentors_data.append(mentor)
        return mentors_data


class MultipleChoiceField(forms.MultipleChoiceField):
    def to_python(self, value):
        return value

    def validate(self, value):
        return value


class _BaseAdminForm(forms.ModelForm):
    mentors_on_page = MultipleChoiceField(
        widget=MentorCheckboxSelectMultiple(), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            page = self.instance.page
            choices = []
            mentors = Mentor.objects.distinct()
            if page.tag:
                mentors = mentors.filter(Q(tags=page.tag) | Q(pages=page))
            elif page.category:
                mentors = mentors.filter(
                    Q(tags__categories=page.category) | Q(pages=page)
                )
            for mentor in mentors:
                page_mentors = PageMentors.objects.filter(
                    page=page, mentor=mentor
                ).first()
                mentor.index = page_mentors.index if page_mentors else -1
                choices.append((mentor, str(mentor)))
            self.fields['mentors_on_page'].choices = choices

    @transaction.atomic
    def save(self, commit=None):
        mentors = self.cleaned_data['mentors_on_page']
        instance = super().save(commit=False)
        instance.save()
        page = instance.page
        if page is not None:
            page.page_mentors.all().delete()
            for mentor in mentors:
                PageMentors.objects.create(page=page, mentor=mentor, index=mentor.index)
        return instance


class _BaseHasMentorFilter(admin.SimpleListFilter, ABC):
    title = "Mentor Association"
    parameter_name = 'mentor_association'

    def lookups(self, request, model_admin):
        return (
            ('associated', "Mentor Associated"),
            ('not_associated', "Mentor Not Associated"),
        )


class CategoryAdminForm(_BaseAdminForm):
    icon = ImageFormField()

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'shortcut': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


class TagInline(admin.TabularInline):
    verbose_name = "Tags"
    model = CategoryTag
    extra = 1


class CategoryHasMentorFilter(_BaseHasMentorFilter):
    def queryset(self, request, queryset):
        if self.value() == 'associated':
            return queryset.filter(tags__mentors__isnull=False).distinct()
        elif self.value() == 'not_associated':
            return queryset.filter(tags__mentors__isnull=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['title', 'shortcut', 'link']
    readonly_fields = ['link', 'display_icon', 'mentors']
    fieldsets = [
        (
            None,
            {
                'fields': [
                    'display_icon',
                    'icon',
                    'title',
                    'shortcut',
                    'link',
                    'mentors_on_page',
                ]
            },
        ),
        ('Mentors', {'fields': ['mentors']}),
    ]
    inlines = [TagInline]

    def link(self, obj):
        url = f"https://{settings.WEB_DOMAIN}/mentors/{obj.shortcut}"
        return format_html('<a href="{}">{}</a>', url, url)

    def display_icon(self, obj):
        return format_html('<img src="{}" width="100"/>', obj.icon.url)

    def mentors(self, obj):
        mentors = Mentor.objects.filter(tags__categories=obj).distinct()
        if mentors.exists():
            return '\n'.join([f"🔹 {mentor}" for mentor in mentors])
        return "No mentors"


class CategoryInline(admin.TabularInline):
    verbose_name = "Categories"
    model = CategoryTag
    extra = 1


class TagAdminForm(_BaseAdminForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
            'shortcut': forms.TextInput(attrs={'style': 'height: 15px; width: 200px'}),
        }


class TagHasMentorFilter(_BaseHasMentorFilter):
    def queryset(self, request, queryset):
        if self.value() == 'associated':
            return queryset.filter(mentors__isnull=False).distinct()
        elif self.value() == 'not_associated':
            return queryset.filter(mentors__isnull=True)


class MentorInline(admin.TabularInline):
    verbose_name = "Mentors"
    model = Mentor.tags.through
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ['title', 'shortcut', 'link']
    fields = ['title', 'shortcut', 'link', 'mentors_on_page']
    readonly_fields = ['link', 'page']
    inlines = [CategoryInline, MentorInline]
    list_filter = [TagHasMentorFilter]

    def link(self, obj):
        url = f"https://{settings.WEB_DOMAIN}/mentors/{obj.shortcut}"
        return format_html('<a href="{}">{}</a>', url, url)
