# Generated by Django 4.2.3 on 2023-07-23 15:15

from django.db import migrations, models

import app.pages.models._links


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='icon',
            field=models.ImageField(
                upload_to=app.pages.models._links.social_link_icon_upload_to
            ),
        ),
    ]
