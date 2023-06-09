from django.db import migrations


def copy_en_to_title_fields(apps, _):
    Category = apps.get_model('tags', 'Category')
    Tag = apps.get_model('tags', 'Tag')
    for obj in Category.objects.all():
        obj.title = obj.title_en or obj.title
        obj.save(update_fields=['title'])
    for obj in Tag.objects.all():
        obj.title = obj.title_en or obj.title
        obj.save(update_fields=['title'])


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0004_remove_tag_category'),
    ]

    operations = [
        migrations.RunPython(copy_en_to_title_fields, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='category',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_ru',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_ru',
        ),
    ]
