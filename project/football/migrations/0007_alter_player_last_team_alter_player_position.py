# Generated by Django 4.1.5 on 2023-07-20 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0006_player_last_team_player_position_alter_player_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="last_team",
            field=models.CharField(default="?", max_length=50),
        ),
        migrations.AlterField(
            model_name="player",
            name="position",
            field=models.CharField(default="?", max_length=4),
        ),
    ]
