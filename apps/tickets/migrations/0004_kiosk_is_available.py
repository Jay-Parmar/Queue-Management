# Generated by Django 4.2.13 on 2024-06-13 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0003_ticket_is_resolved"),
    ]

    operations = [
        migrations.AddField(
            model_name="kiosk",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]
