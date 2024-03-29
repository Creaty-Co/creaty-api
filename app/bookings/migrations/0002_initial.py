# Generated by Django 4.2.2 on 2023-06-27 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('mentors', '0001_initial'),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialbooking',
            name='mentor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='free_bookings',
                to='mentors.mentor',
            ),
        ),
        migrations.AddField(
            model_name='packagebooking',
            name='mentor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='package_bookings',
                to='mentors.mentor',
            ),
        ),
        migrations.AddField(
            model_name='packagebooking',
            name='package',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bookings',
                to='mentors.package',
            ),
        ),
        migrations.AddField(
            model_name='hourlybooking',
            name='mentor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='hourly_bookings',
                to='mentors.mentor',
            ),
        ),
    ]
