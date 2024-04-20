# Generated by Django 4.2.6 on 2024-04-18 14:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mentors', '0002_remove_mentor_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentor',
            name='link',
        ),
        migrations.AddField(
            model_name='mentor',
            name='links',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.URLField(), blank=True, default=list, size=None
            ),
        ),
    ]