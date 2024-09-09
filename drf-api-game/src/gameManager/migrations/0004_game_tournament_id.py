# Generated by Django 5.0.3 on 2024-08-28 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameManager', '0003_game_player1_name_game_player2_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='tournament_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gameManager.tournament'),
        ),
    ]
