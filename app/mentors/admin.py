from django.contrib import admin

from app.mentors.models import Mentor, MentorInfo


class MentorInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume')


class MentorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


admin.site.register(MentorInfo, MentorInfoAdmin)
admin.site.register(Mentor, MentorAdmin)
