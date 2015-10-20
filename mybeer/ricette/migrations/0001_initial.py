# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoppiaCottura',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tempo', models.CharField(max_length=10)),
                ('temperatura', models.IntegerField(default=30, max_length=3)),
                ('messaggio', models.CharField(default=b'', max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ricetta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(max_length=12)),
                ('titolo', models.CharField(max_length=256)),
                ('descrizione', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('coppia_cottura', models.ManyToManyField(to='ricette.CoppiaCottura', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
