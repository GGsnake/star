# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chanelroute',
            name='ChanelMessage',
        ),
        migrations.AddField(
            model_name='chanelroute',
            name='ChanelNumbers',
            field=models.CharField(verbose_name='波道编号', max_length=80, blank=True, null=True, default=''),
        ),
        migrations.RemoveField(
            model_name='chanelroute',
            name='ChanelNumber',
        ),
        migrations.AddField(
            model_name='chanelroute',
            name='ChanelNumber',
            field=models.ManyToManyField(blank=True, null=True, to='adc.Channel'),
        ),
    ]
