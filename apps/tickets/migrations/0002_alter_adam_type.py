# Generated by Django 4.2.13 on 2024-06-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adam",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CREATE_TICKET", "CREATE_TICKET"),
                    ("ASSIGN_KIOSK", "ASSIGN_KIOSK"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
