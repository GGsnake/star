# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('MainMan', models.CharField(verbose_name='光缆主负责人', max_length=80, blank=True, null=True, default='')),
                ('To', models.CharField(verbose_name='所属地', max_length=80, blank=True, null=True, default='')),
                ('BkMan', models.CharField(verbose_name='光缆备份负责人', max_length=80, blank=True, null=True, default='')),
                ('Cablename', models.CharField(verbose_name='光缆编号', max_length=80, blank=True, null=True, default='')),
                ('Sup', models.CharField(verbose_name='供应商', max_length=80, blank=True, null=True, default='')),
                ('Apoint', models.CharField(verbose_name='A端编号', max_length=80, blank=True, null=True, default='')),
                ('Bpoint', models.CharField(verbose_name='B端编号', max_length=80, blank=True, null=True, default='')),
                ('Apointadd', models.CharField(verbose_name='A端地址', max_length=80, blank=True, null=True, default='')),
                ('Bpointadd', models.CharField(verbose_name='B端地址', max_length=80, blank=True, null=True, default='')),
                ('FinshDate', models.CharField(verbose_name='完工时间', max_length=80, blank=True, null=True, default='')),
                ('Distance', models.CharField(verbose_name='距离', max_length=80, blank=True, null=True, default='')),
                ('Corenumber', models.CharField(verbose_name='芯数', max_length=80, blank=True, null=True, default='')),
                ('Contractnumber', models.CharField(verbose_name='合同编号', max_length=80, blank=True, null=True, default='')),
                ('BusinessMan', models.CharField(verbose_name='商务对口人', max_length=80, blank=True, null=True, default='')),
                ('ProtectMan', models.CharField(verbose_name='维护联系人', max_length=80, blank=True, null=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ChanelRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Mainman', models.CharField(verbose_name='波道主负责人', max_length=80, blank=True, null=True, default='')),
                ('BkMan', models.CharField(verbose_name='波道路由备份负责人', max_length=80, blank=True, null=True, default='')),
                ('Business', models.CharField(verbose_name='业务', max_length=80, blank=True, null=True, default='')),
                ('Customer', models.CharField(verbose_name='客户', max_length=80, blank=True, null=True, default='')),
                ('ChanelRouteNumber', models.CharField(verbose_name='路由编号', max_length=80, blank=True, null=True, default='')),
                ('ChanelMessage', models.CharField(verbose_name='波分信息', max_length=80, blank=True, null=True, default='')),
                ('ChanelNumber', models.CharField(verbose_name='波道编号', max_length=80, blank=True, null=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Business', models.CharField(verbose_name='业务', max_length=80, blank=True, null=True, default='')),
                ('Customer', models.CharField(verbose_name='客户', max_length=80, blank=True, null=True, default='')),
                ('Mainman', models.CharField(verbose_name='波道负责人', max_length=80, blank=True, null=True, default='')),
                ('BkMan', models.CharField(verbose_name='波道备份负责人', max_length=80, blank=True, null=True, default='')),
                ('Firbenumber', models.CharField(verbose_name='光纤编号', max_length=80, blank=True, null=True, default='')),
                ('Channelname', models.CharField(verbose_name='波道编号', max_length=80, blank=True, null=True, default='')),
                ('Acap', models.CharField(verbose_name='A机柜', max_length=80, blank=True, null=True, default='')),
                ('Bcap', models.CharField(verbose_name='B机柜', max_length=80, blank=True, null=True, default='')),
                ('Aposition', models.CharField(verbose_name='A机位', max_length=80, blank=True, null=True, default='')),
                ('Bposition', models.CharField(verbose_name='B机位', max_length=80, blank=True, null=True, default='')),
                ('STATE', models.CharField(verbose_name='波道状态', max_length=80, blank=True, null=True, default='')),
                ('CORE', models.CharField(verbose_name='多芯', max_length=80, blank=True, null=True, default='')),
                ('TYPE', models.CharField(verbose_name='波道类型', max_length=80, blank=True, null=True, default='')),
                ('AChannel', models.CharField(verbose_name='A波道', max_length=80, blank=True, null=True, default='')),
                ('BChannel', models.CharField(verbose_name='B波道', max_length=80, blank=True, null=True, default='')),
                ('Aequipment', models.CharField(verbose_name='A设备', max_length=80, blank=True, null=True, default='')),
                ('Bequipment', models.CharField(verbose_name='B设备', max_length=80, blank=True, null=True, default='')),
                ('Aassets', models.CharField(verbose_name='A资产编号', max_length=80, blank=True, null=True, default='')),
                ('Bassets', models.CharField(verbose_name='A资产编号', max_length=80, blank=True, null=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Clicent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Fibre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('MainMan', models.CharField(verbose_name='光纤主负责人', max_length=80, blank=True, null=True, default='')),
                ('BkMan', models.CharField(verbose_name='光纤备份负责人', max_length=80, blank=True, null=True, default='')),
                ('STATE', models.CharField(verbose_name='光纤状态', max_length=80, blank=True, null=True, default='')),
                ('StartData', models.CharField(verbose_name='光纤分配时间', max_length=80, blank=True, null=True, default='')),
                ('FibreName', models.CharField(verbose_name='光纤编号', max_length=80, blank=True, null=True, default='')),
                ('Acap', models.CharField(verbose_name='A机柜', max_length=80, blank=True, null=True, default='')),
                ('Bcap', models.CharField(verbose_name='B机柜', max_length=80, blank=True, null=True, default='')),
                ('Aposition', models.CharField(verbose_name='A机位', max_length=80, blank=True, null=True, default='')),
                ('Bposition', models.CharField(verbose_name='B机位', max_length=80, blank=True, null=True, default='')),
                ('Aport', models.CharField(verbose_name='A端子', max_length=80, blank=True, null=True, default='')),
                ('Bport', models.CharField(verbose_name='B端子', max_length=80, blank=True, null=True, default='')),
                ('Cable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adc.Cable')),
            ],
        ),
        migrations.CreateModel(
            name='ImportTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Time', models.CharField(verbose_name='操作时间', max_length=80, blank=True, null=True, default='')),
                ('Name', models.CharField(verbose_name='文件名', max_length=80, blank=True, null=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='Firbes',
            field=models.ManyToManyField(blank=True, null=True, to='adc.Fibre'),
        ),
    ]
