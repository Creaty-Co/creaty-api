# Generated by Django 3.2.2 on 2022-07-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0007_auto_20220226_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorinfo',
            name='portfolio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentorinfo',
            name='portfolio_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentorinfo',
            name='portfolio_ru',
            field=models.TextField(blank=True, null=True),
        ),
    ]
