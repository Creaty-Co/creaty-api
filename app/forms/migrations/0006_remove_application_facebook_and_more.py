# Generated by Django 4.2.2 on 2023-06-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forms', '0005_alter_field_type_alter_form_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='application',
            name='telegram',
        ),
        migrations.RemoveField(
            model_name='application',
            name='viber',
        ),
        migrations.RemoveField(
            model_name='application',
            name='whats_app',
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.TextField(
                choices=[
                    ('name', 'Name'),
                    ('email', 'Email'),
                    ('about', 'About the issue'),
                    ('link', 'Profile link'),
                ]
            ),
        ),
    ]
