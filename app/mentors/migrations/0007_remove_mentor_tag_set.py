# Generated by Django 4.2.2 on 2023-06-08 14:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentors', '0006_mentor_link_mentor_tags_alter_mentor_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentor',
            name='tag_set',
        ),
    ]