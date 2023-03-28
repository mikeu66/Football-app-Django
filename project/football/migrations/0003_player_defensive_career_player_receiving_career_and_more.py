# Generated by Django 4.1.5 on 2023-03-20 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0002_player_passing_career"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="defensive_career",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="receiving_career",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="rushing_career",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="scoring_career",
            field=models.TextField(null=True),
        ),
    ]
