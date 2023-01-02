# Generated by Django 3.2.2 on 2022-02-03 18:29

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Form',
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
                    'type',
                    models.TextField(
                        choices=[
                            ('become_mentor', 'Станьте ментором'),
                            ('choose_mentor', 'Получить помощь в подборе ментора'),
                            ('test_meeting', 'Беспатная тестовая встреча'),
                            ('still_questions', 'Ещё остались вопросы'),
                        ],
                        unique=True,
                    ),
                ),
                ('description', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('post_send', models.TextField()),
                ('post_send_ru', models.TextField(null=True)),
                ('post_send_en', models.TextField(null=True)),
                (
                    'fields',
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.TextField(
                            choices=[
                                ('name', 'Имя'),
                                ('email', 'Email'),
                                ('telegram', 'Telegram'),
                                ('facebook', 'Facebook messanger'),
                                ('whats_app', 'WhatsApp'),
                                ('viber', 'Viber'),
                                ('about', 'О себе'),
                            ]
                        ),
                        size=None,
                    ),
                ),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Application',
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
                ('name', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telegram', models.TextField(blank=True, null=True)),
                ('facebook', models.TextField(blank=True, null=True)),
                ('whats_app', models.TextField(blank=True, null=True)),
                ('viber', models.TextField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                (
                    'form',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='forms.form'
                    ),
                ),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
    ]
