# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0002_auto_20180313_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('logname', models.CharField(max_length=80)),
                ('Credate', models.DateTimeField(auto_now_add=True)),
                ('userid', models.CharField(max_length=80)),
                ('Changedate', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=80)),
            ],
        ),
    ]
