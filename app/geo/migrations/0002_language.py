# Generated by Django 3.2.2 on 2022-02-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('code', models.CharField(max_length=6, unique=True)),
                ('name', models.TextField()),
                ('name_ru', models.TextField(null=True)),
                ('name_en', models.TextField(null=True)),
                ('name_native', models.TextField()),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
    ]
