# Generated by Django 4.1.5 on 2023-07-20 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0007_alter_player_last_team_alter_player_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="last_team",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="player", name="position", field=models.CharField(max_length=4),
        ),
    ]