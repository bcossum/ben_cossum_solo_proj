# Generated by Django 2.2 on 2020-12-13 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_game_tracker_app', '0005_auto_20201213_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
