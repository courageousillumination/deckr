# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deckr', '0002_gamedefinition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedefinition',
            name='path',
            field=models.FilePathField(
                path=b'/home/tristan/development/deckr/webapp/game_defs',
                allow_folders=True),
            preserve_default=True,
        ),
    ]
