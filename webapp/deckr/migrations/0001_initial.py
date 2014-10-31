# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_id', models.IntegerField()),
                ('max_players', models.IntegerField(default=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player_id', models.IntegerField()),
                ('nickname', models.CharField(max_length=128)),
                ('game_room', models.ForeignKey(to='deckr.GameRoom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
