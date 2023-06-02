from django.db import migrations


def copy_en_to_placeholder_description_post_send(apps, schema_editor):
    Field = apps.get_model('forms', 'Field')
    Form = apps.get_model('forms', 'Form')
    for obj in Field.objects.all():
        obj.placeholder = obj.placeholder_en or obj.placeholder or ''
        obj.save(update_fields=['placeholder'])
    for obj in Form.objects.all():
        obj.description = obj.description_en or obj.description or ''
        obj.post_send = obj.post_send_en or obj.post_send or ''
        obj.save(update_fields=['description', 'post_send'])


class Migration(migrations.Migration):
    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            copy_en_to_placeholder_description_post_send, migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='field',
            name='placeholder_en',
        ),
        migrations.RemoveField(
            model_name='field',
            name='placeholder_ru',
        ),
        migrations.RemoveField(
            model_name='form',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='form',
            name='post_send_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='post_send_ru',
        ),
    ]
