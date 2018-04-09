# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0003_log'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Clicent',
        ),
        migrations.DeleteModel(
            name='ImportTime',
        ),
        migrations.AddField(
            model_name='log',
            name='type',
            field=models.CharField(max_length=80, default=1),
            preserve_default=False,
        ),
    ]
