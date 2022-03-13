# Generated by Django 3.2.2 on 2022-03-13 11:15

import uuid

from django.db import migrations


def gen_uuid(apps, _):
    Subscriber = apps.get_model('mailings', 'Subscriber')
    for subscriber in Subscriber.objects.all():
        subscriber.uuid = uuid.uuid4()
        subscriber.save(update_fields=['uuid'])


class Migration(migrations.Migration):
    
    dependencies = [
        ('mailings', '0004_subscriber_uuid'),
    ]
    
    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
