# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deckr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameDefinition',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('path', models.FilePathField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
