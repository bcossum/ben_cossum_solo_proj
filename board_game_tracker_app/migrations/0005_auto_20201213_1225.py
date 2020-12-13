# Generated by Django 2.2 on 2020-12-13 20:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('board_game_tracker_app', '0004_auto_20201211_0005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='play',
            options={'ordering': ('date',)},
        ),
        migrations.AlterField(
            model_name='play',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 12, 13, 20, 25, 40, 332465, tzinfo=utc)),
        ),
    ]
