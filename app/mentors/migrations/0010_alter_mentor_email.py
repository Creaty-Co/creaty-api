# Generated by Django 4.2.2 on 2023-06-21 15:22

from django.db import migrations, models

from app.base.tests.fakers import fake


def randomize_blank_mentor_emails(apps, _):
    Mentor = apps.get_model('mentors', 'Mentor')
    for mentor in Mentor.objects.filter(email=''):
        mentor.email = f"fake_{fake.email()}"
        mentor.save()


class Migration(migrations.Migration):
    dependencies = [('mentors', '0009_alter_mentor_email')]

    operations = [
        migrations.RunPython(randomize_blank_mentor_emails),
        migrations.AlterField(
            model_name='mentor',
            name='email',
            field=models.EmailField(db_index=True, max_length=254),
        ),
    ]
