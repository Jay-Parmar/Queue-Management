# Generated by Django 4.2.13 on 2024-06-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0002_alter_adam_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="is_resolved",
            field=models.BooleanField(default=False),
        ),
    ]
