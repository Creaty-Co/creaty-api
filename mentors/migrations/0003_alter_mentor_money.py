# Generated by Django 3.2.2 on 2022-02-01 19:01

import djmoney.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0002_auto_20220201_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='money',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=10),
        ),
    ]
