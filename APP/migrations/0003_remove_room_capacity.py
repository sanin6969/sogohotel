# Generated by Django 5.0.6 on 2024-06-07 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_room_is_booked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='capacity',
        ),
    ]
