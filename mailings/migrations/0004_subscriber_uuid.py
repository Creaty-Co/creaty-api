# Generated by Django 3.2.2 on 2022-03-13 10:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0003_mailing_is_stopped'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
