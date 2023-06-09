# Generated by Django 4.2.2 on 2023-06-09 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forms', '0004_application_link_alter_field_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.TextField(
                choices=[
                    ('name', 'Name'),
                    ('email', 'Email'),
                    ('telegram', 'Telegram'),
                    ('facebook', 'Facebook messenger'),
                    ('whats_app', 'WhatsApp'),
                    ('viber', 'Viber'),
                    ('about', 'About the issue'),
                    ('link', 'Profile link'),
                ]
            ),
        ),
        migrations.AlterField(
            model_name='form',
            name='type',
            field=models.TextField(
                choices=[
                    ('become_mentor', 'Become a mentor'),
                    ('choose_mentor', 'Get help choosing a mentor'),
                    ('test_meeting', 'Free test meeting'),
                    ('still_questions', 'Still have questions'),
                    ('signup_mentor', 'Sign up for a mentor'),
                ],
                unique=True,
            ),
        ),
    ]
