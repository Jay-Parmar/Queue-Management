# Generated by Django 4.2.13 on 2024-06-15 10:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0012_reports"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Reports",
            new_name="Report",
        ),
    ]
