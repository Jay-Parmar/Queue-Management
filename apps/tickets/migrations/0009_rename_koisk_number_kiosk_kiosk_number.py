# Generated by Django 4.2.13 on 2024-06-13 11:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0008_rename_related_button_adam_kiosk"),
    ]

    operations = [
        migrations.RenameField(
            model_name="kiosk",
            old_name="koisk_number",
            new_name="kiosk_number",
        ),
    ]