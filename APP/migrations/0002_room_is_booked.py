# Generated by Django 5.0.6 on 2024-06-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
