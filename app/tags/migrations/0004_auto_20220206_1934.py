# Generated by Django 3.2.2 on 2022-02-06 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20220206_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='shortcut',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='shortcut',
            field=models.TextField(unique=True),
        ),
    ]
