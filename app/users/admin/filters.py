from django.contrib import admin


class IsMentorFilter(admin.SimpleListFilter):
    title = "Is mentor"
    parameter_name = 'is_mentor'

    def lookups(self, request, model_admin):
        return (('True', "Yes"), ('False', "No"))

    def queryset(self, request, queryset):
        match self.value():
            case 'True':
                return queryset.filter(mentor__isnull=False)
            case 'False':
                return queryset.filter(mentor__isnull=True)
