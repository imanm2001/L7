# Generated by Django 4.2.4 on 2023-09-05 09:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("HW", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("uid", models.IntegerField(default=0)),
                ("filename", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
