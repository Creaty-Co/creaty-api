# Generated by Django 4.2.1 on 2023-06-02 16:27

from django.db import migrations


def copy_en_to_name(apps, schema_editor):
    Country = apps.get_model('geo', 'Country')
    Language = apps.get_model('geo', 'Language')
    for obj in Country.objects.all():
        obj.name = obj.name_en or obj.name
        obj.save(update_fields=['name'])
    for obj in Language.objects.all():
        obj.name = obj.name_en or obj.name
        obj.save(update_fields=['name'])


class Migration(migrations.Migration):
    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_en_to_name, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='country',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='country',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='language',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='language',
            name='name_ru',
        ),
    ]