# Generated by Django 3.2.2 on 2022-02-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0005_alter_package_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='first_name_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='first_name_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='last_name_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='last_name_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='profession_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='profession_ru',
            field=models.TextField(blank=True, null=True),
        ),
    ]
