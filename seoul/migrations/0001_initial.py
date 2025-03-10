# Generated by Django 5.1.6 on 2025-02-24 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Place",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("district", models.CharField(max_length=10)),
                ("place_image", models.ImageField(upload_to="place_images/")),
                ("address", models.TextField(verbose_name="주소")),
                ("description", models.TextField()),
            ],
        ),
    ]
