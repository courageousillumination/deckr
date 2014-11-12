# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deckr', '0003_auto_20141106_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameroom',
            name='game_definition',
            field=models.ForeignKey(to='deckr.GameDefinition', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gamedefinition',
            name='path',
            field=models.FilePathField(
                path=b'/media/development/deckr/webapp/game_defs',
                allow_folders=True),
            preserve_default=True,
        ),
    ]
