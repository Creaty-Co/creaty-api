from django.db import migrations


def copy_en_to_faq_fields(apps, schema_editor):
    Faq = apps.get_model('pages', 'Faq')
    for obj in Faq.objects.all():
        obj.answer = obj.answer_en
        obj.question = obj.question_en
        obj.save(update_fields=['answer', 'question'])


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_en_to_faq_fields, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='faq',
            name='answer_en',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='answer_ru',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='question_en',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='question_ru',
        ),
    ]
