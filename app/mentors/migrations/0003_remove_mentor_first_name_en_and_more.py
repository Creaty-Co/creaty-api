from django.db import migrations


def copy_en_to_mentor_and_mentorinfo_fields(apps, schema_editor):
    Mentor = apps.get_model('mentors', 'Mentor')
    MentorInfo = apps.get_model('mentors', 'MentorInfo')
    for obj in Mentor.objects.all():
        obj.first_name = obj.first_name_en
        obj.last_name = obj.last_name_en
        obj.profession = obj.profession_en
        obj.save(update_fields=['first_name', 'last_name', 'profession'])
    for obj in MentorInfo.objects.all():
        obj.experience = obj.experience_en
        obj.resume = obj.resume_en
        obj.what_help = obj.what_help_en
        obj.save(update_fields=['experience', 'resume', 'what_help'])


class Migration(migrations.Migration):
    dependencies = [
        ('mentors', '0002_mentor_is_draft'),
    ]

    operations = [
        migrations.RunPython(
            copy_en_to_mentor_and_mentorinfo_fields, migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='first_name_en',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='first_name_ru',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='last_name_en',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='last_name_ru',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='profession_en',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='profession_ru',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='experience_en',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='experience_ru',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='resume_en',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='resume_ru',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='what_help_en',
        ),
        migrations.RemoveField(
            model_name='mentorinfo',
            name='what_help_ru',
        ),
    ]
