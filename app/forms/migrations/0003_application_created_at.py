# Generated by Django 4.2.1 on 2023-06-06 15:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forms', '0002_remove_field_placeholder_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]