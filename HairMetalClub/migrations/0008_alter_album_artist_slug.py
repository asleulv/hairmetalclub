# Generated by Django 4.2.4 on 2023-09-05 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("HairMetalClub", "0007_alter_album_highlights_alter_album_lowlights"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="artist_slug",
            field=models.SlugField(),
        ),
    ]
