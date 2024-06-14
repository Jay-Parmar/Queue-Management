# Generated by Django 4.2.13 on 2024-06-13 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0009_rename_koisk_number_kiosk_kiosk_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adam",
            name="kiosk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tickets.kiosk",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="kiosk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tickets.kiosk",
            ),
        ),
    ]
