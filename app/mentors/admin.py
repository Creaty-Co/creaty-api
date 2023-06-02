from django.contrib import admin

from app.mentors.models import Mentor, MentorInfo, Package


class MentorInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume')


class MentorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'packages')


class PackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(MentorInfo, MentorInfoAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Package, PackageAdmin)
