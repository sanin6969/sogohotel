# Generated by Django 5.0.6 on 2024-06-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("APP", "0003_remove_room_capacity"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="booked_checkin_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="room",
            name="booked_checkout_date",
            field=models.DateTimeField(null=True),
        ),
    ]