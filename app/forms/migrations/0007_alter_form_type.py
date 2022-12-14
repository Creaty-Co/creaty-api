# Generated by Django 3.2.2 on 2022-07-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_auto_20220613_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='type',
            field=models.TextField(
                choices=[
                    ('become_mentor', 'Станьте ментором'),
                    ('choose_mentor', 'Получить помощь в подборе ментора'),
                    ('test_meeting', 'Беспатная тестовая встреча'),
                    ('still_questions', 'Ещё остались вопросы'),
                    ('signup_mentor', 'Записаться к ментору'),
                ],
                unique=True,
            ),
        ),
    ]
