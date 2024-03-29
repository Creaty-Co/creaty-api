# Generated by Django 4.2.3 on 2023-07-22 20:06

from django.db import migrations, models

import app.users.models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(
                blank=True, null=True, upload_to=app.users.models.user_avatar_upload_to
            ),
        ),
    ]
