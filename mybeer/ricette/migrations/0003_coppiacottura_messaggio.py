# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ricette', '0002_remove_coppiacottura_messaggio'),
    ]

    operations = [
        migrations.AddField(
            model_name='coppiacottura',
            name='messaggio',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
    ]
