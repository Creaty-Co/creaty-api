# Generated by Django 4.1.5 on 2023-01-22 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0007_alter_subscriber_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='subscriber',
            options={'ordering': ['pk']},
        ),
    ]
