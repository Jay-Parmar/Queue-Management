# Generated by Django 4.2.13 on 2024-06-13 11:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0007_adam_related_button"),
    ]

    operations = [
        migrations.RenameField(
            model_name="adam",
            old_name="related_button",
            new_name="kiosk",
        ),
    ]