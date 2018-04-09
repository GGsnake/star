from django.contrib.auth.models import AbstractUser, User
from django.db import models

from django import forms
from django.http import Http404
from django.shortcuts import render


class Cable(models.Model):
    # 光缆主负责人
    MainMan = models.CharField(max_length=80, null=True, verbose_name='光缆主负责人', blank=True, default="")
    # 所属地
    To = models.CharField(max_length=80, null=True, verbose_name='所属地', blank=True, default="")
    # 光缆备份负责人
    BkMan = models.CharField(max_length=80, null=True, verbose_name='光缆备份负责人', blank=True, default="")
    # 光缆编号
    Cablename = models.CharField(max_length=80, null=True, verbose_name='光缆编号', blank=True, default="")
    # 供应商
    Sup = models.CharField(max_length=80, null=True, verbose_name='供应商', blank=True, default="")
    # A端编号
    Apoint = models.CharField(max_length=80, null=True, verbose_name='A端编号', blank=True, default="")
    # B端编号
    Bpoint = models.CharField(max_length=80, null=True, verbose_name='B端编号', blank=True, default="")
    # A端地址
    Apointadd = models.CharField(max_length=80, null=True, verbose_name='A端地址', blank=True, default="")
    # B端地址
    Bpointadd = models.CharField(max_length=80, null=True, verbose_name='B端地址', blank=True, default="")
    # 完工时间
    FinshDate = models.CharField(max_length=80, null=True, verbose_name='完工时间', blank=True, default="")
    # 距离
    Distance = models.CharField(max_length=80, null=True, verbose_name='距离', blank=True, default="")
    # 芯数
    Corenumber = models.CharField(max_length=80, null=True, verbose_name='芯数', blank=True, default="")
    # 合同编号
    Contractnumber = models.CharField(max_length=80, null=True, verbose_name='合同编号', blank=True, default="")
    # 商务对口人
    BusinessMan = models.CharField(max_length=80, null=True, verbose_name='商务对口人', blank=True, default="")
    # 维护联系人
    ProtectMan = models.CharField(max_length=80, null=True, verbose_name='维护联系人', blank=True, default="")

    def __str__(self):
        return self.Cablename


class Fibre(models.Model):
    # 光纤主负责人
    MainMan = models.CharField(max_length=80, null=True, verbose_name='光纤主负责人', blank=True, default="")
    # 光纤备份负责人
    BkMan = models.CharField(max_length=80, null=True, verbose_name='光纤备份负责人', blank=True, default="")
    # 光纤状态
    STATE = models.CharField(max_length=80, null=True, verbose_name='光纤状态', blank=True, default="")
    # 所属光缆
    Cable = models.ForeignKey(Cable, blank=True, null=True, on_delete=models.SET_NULL)
    # 光纤分配时间
    StartData = models.CharField(max_length=80, null=True, verbose_name='光纤分配时间', blank=True, default="")
    # 光纤编号
    FibreName = models.CharField(max_length=80, null=True, verbose_name='光纤编号', blank=True, default="")
    # A机柜
    Acap = models.CharField(max_length=80, null=True, verbose_name='A机柜', blank=True, default="")
    # B机柜
    Bcap = models.CharField(max_length=80, null=True, verbose_name='B机柜', blank=True, default="")
    # A机位
    Aposition = models.CharField(max_length=80, null=True, verbose_name='A机位', blank=True, default="")
    # B机位
    Bposition = models.CharField(max_length=80, null=True, verbose_name='B机位', blank=True, default="")
    # A端子
    Aport = models.CharField(max_length=80, null=True, verbose_name='A端子', blank=True, default="")
    # B端子
    Bport = models.CharField(max_length=80, null=True, verbose_name='B端子', blank=True, default="")


class Channel(models.Model):
    # 业务
    Business = models.CharField(max_length=80, null=True, verbose_name='业务', blank=True, default="")
    # 客户
    Customer = models.CharField(max_length=80, null=True, verbose_name='客户', blank=True, default="")
    # 波道主负责人
    Mainman = models.CharField(max_length=80, null=True, verbose_name='波道负责人', blank=True, default="")
    # 波道备份负责人
    BkMan = models.CharField(max_length=80, null=True, verbose_name='波道备份负责人', blank=True, default="")
    # 光纤编号
    Firbenumber = models.CharField(max_length=80, null=True, verbose_name='光纤编号', blank=True, default="")
    # 波道编号
    Channelname = models.CharField(max_length=80, null=True, verbose_name='波道编号', blank=True, default="")
    # A机柜
    Acap = models.CharField(max_length=80, null=True, verbose_name='A机柜', blank=True, default="")
    # B机柜
    Bcap = models.CharField(max_length=80, null=True, verbose_name='B机柜', blank=True, default="")
    # A机位
    Aposition = models.CharField(max_length=80, null=True, verbose_name='A机位', blank=True, default="")
    # B机位
    Bposition = models.CharField(max_length=80, null=True, verbose_name='B机位', blank=True, default="")
    # 波道状态
    STATE = models.CharField(max_length=80, null=True, verbose_name='波道状态', blank=True, default="")
    # 多芯
    CORE = models.CharField(max_length=80, null=True, verbose_name='多芯', blank=True, default="")
    # 波道类型
    TYPE = models.CharField(max_length=80, null=True, verbose_name='波道类型', blank=True, default="")

    # 所属光纤

    Firbes = models.ManyToManyField(Fibre, null=True, blank=True)

    # A波道
    AChannel = models.CharField(max_length=80, null=True, verbose_name='A波道', blank=True, default="")
    # B波道
    BChannel = models.CharField(max_length=80, null=True, verbose_name='B波道', blank=True, default="")
    # A设备
    Aequipment = models.CharField(max_length=80, null=True, verbose_name='A设备', blank=True, default="")
    # B设备
    Bequipment = models.CharField(max_length=80, null=True, verbose_name='B设备', blank=True, default="")
    # A资产编号
    Aassets = models.CharField(max_length=80, null=True, verbose_name='A资产编号', blank=True, default="")
    # B资产编号
    Bassets = models.CharField(max_length=80, null=True, verbose_name='A资产编号', blank=True, default="")


class ChanelRoute(models.Model):
    # 波道路由主负责人
    Mainman = models.CharField(max_length=80, null=True, verbose_name='波道主负责人', blank=True, default="")
    # 波道路由备份负责人
    BkMan = models.CharField(max_length=80, null=True, verbose_name='波道路由备份负责人', blank=True, default="")

    # 业务
    Business = models.CharField(max_length=80, null=True, verbose_name='业务', blank=True, default="")
    # 客户
    Customer = models.CharField(max_length=80, null=True, verbose_name='客户', blank=True, default="")
    # 路由编号
    ChanelRouteNumber = models.CharField(max_length=80, null=True, verbose_name='路由编号', blank=True, default="")
    # 波道编号\
    ChanelNumber = models.ManyToManyField(Channel, null=True, blank=True)
    # 波道编号\
    ChanelNumbers = models.CharField(max_length=80, null=True, verbose_name='波道编号', blank=True, default="")


class log(models.Model):
    # 客户名字
    logname = models.CharField(max_length=80)
    Credate = models.DateTimeField(auto_now_add=True)
    userid=models.CharField(max_length=80)
    Changedate = models.DateTimeField(auto_now=True)
    type= models.CharField(max_length=80)
    content = models.CharField(max_length=80)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

