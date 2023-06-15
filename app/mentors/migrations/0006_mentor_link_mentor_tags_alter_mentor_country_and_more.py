# Generated by Django 4.2.2 on 2023-06-08 13:51

import django.db.models.deletion
from django.db import migrations, models


def move_tag_set_to_tags(apps, _):
    Mentor = apps.get_model('mentors', 'Mentor')
    for mentor in Mentor.objects.all():
        mentor.tags.set(mentor.tag_set.all())


class Migration(migrations.Migration):
    dependencies = [
        ('geo', '0002_remove_country_name_en_remove_country_name_ru_and_more'),
        ('tags', '0005_remove_category_title_en_remove_category_title_ru_and_more'),
        ('mentors', '0005_remove_mentor_info_delete_mentorinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='link',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='mentor',
            name='tags',
            field=models.ManyToManyField(related_name='mentors', to='tags.tag'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='country',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='mentors',
                to='geo.country',
            ),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='languages',
            field=models.ManyToManyField(related_name='mentors', to='geo.language'),
        ),
        migrations.RunPython(move_tag_set_to_tags),
    ]