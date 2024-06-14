# Generated by Django 4.2.13 on 2024-06-13 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0006_alter_adam_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="adam",
            name="related_button",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tickets.kiosk",
            ),
        ),
    ]