# Generated by Django 4.2.4 on 2023-08-13 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("HairMetalClub", "0005_alter_album_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="rating",
            field=models.PositiveIntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")],
                default=1,
            ),
        ),
    ]
