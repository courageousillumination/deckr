# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deckr', '0004_auto_20141112_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedefinition',
            name='path',
            field=models.FilePathField(
                path=b'game_defs',
                allow_files=False,
                allow_folders=True),
            preserve_default=True,
        ),
    ]
