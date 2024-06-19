# Generated by Django 4.2.7 on 2024-06-19 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('title', models.TextField()),
                ('google_event_uuid', models.UUIDField(unique=True)),
                (
                    'guests',
                    models.ManyToManyField(
                        related_name='calendar_events_by_guests',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'host',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='calendar_events_by_host',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
    ]
