# Generated by Django 4.2.2 on 2023-06-27 10:32

import uuid

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Mailing',
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
                ('subject', models.TextField()),
                ('content', models.TextField()),
                ('is_stopped', models.BooleanField(default=True)),
                (
                    'task_ids',
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.TextField(), blank=True, null=True, size=None
                    ),
                ),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
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
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
    ]
