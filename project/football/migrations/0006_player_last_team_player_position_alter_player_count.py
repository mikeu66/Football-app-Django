# Generated by Django 4.1.5 on 2023-07-20 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0005_player_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="player", name="last_team", field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="player", name="position", field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="player", name="count", field=models.IntegerField(default=1),
        ),
    ]