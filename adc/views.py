import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

import math
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from adc import logprint
from adc.models import Cable, Fibre, Channel, ChanelRoute, log


@login_required
def FibeView(request):
    Fb = Fibre.objects.all()
    size=len(Fb)
    ok = len(Fb.filter(STATE="已使用"))
    nook = len(Fb.filter(STATE="未分配"))
    eoor = len(Fb.filter(STATE="故障"))
    logprint.loge("查看光纤".encode("utf-8"), request.user.username, "", "query")
    return render(request, 'polls/FibeView.html', {"ok": ok, "nook": nook, "eoor": eoor, "size": size})


@login_required
def Cabview(request):
    Fb = Cable.objects.all()
    paginator = Paginator(Fb, 8)  # 每页显示25条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    logprint.loge("查看光缆".encode("utf-8"), request.user.username, "", "query")
    return render(request, 'polls/CableView.html', {"c": contacts})


@login_required
def ChannelView(request):
    logprint.loge("查看波道".encode("utf-8"), request.user.username, "", "query")

    return render(request, 'polls/Channel.html')\

@login_required
def lgcat(request):
    return render(request, 'polls/lgcat.html')
def Wsr(request):
    logprint.loge("查看路由", request.user.username, "", "query")
    return render(request, 'polls/WsRou.html')
def search(request):
    if request.user.is_superuser:

        page = int(request.GET.get('page', 1))
        pagesize = int(request.GET.get('pagesize', 8))
        q = request.GET.get('q')

        if not q:
            logdata=log.objects.all().order_by("-pk")[
                  (page - 1) * pagesize:page * pagesize]
            Modellist = []
            for ResultChild in logdata:
                # 临时存储单个结果的字典
                dictchid = {}
                dictchid['logname'] = ResultChild.logname
                dictchid['id'] = ResultChild.pk
                dictchid['Credate'] = ResultChild.Credate.strftime("%Y-%m-%d %H:%M:%S")
                dictchid['userid'] = ResultChild.userid
                dictchid['content'] = ResultChild.content
                Modellist.append(dictchid)
            map = math.ceil(log.objects.all().count()/ pagesize)
            return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
        logdata = log.objects.filter(
            Q(logname__icontains=q) | Q(userid__icontains=q) | Q(content__icontains=q))[
                  (page - 1) * pagesize:page * pagesize]
        Modellist=[]
        for ResultChild in logdata:
            # 临时存储单个结果的字典
            dictchid = {}
            dictchid['logname'] = ResultChild.logname
            dictchid['id'] = ResultChild.pk
            dictchid['Credate'] = ResultChild.Credate.strftime("%Y-%m-%d %H:%M:%S")
            dictchid['userid'] = ResultChild.userid
            dictchid['content'] = ResultChild.content
            Modellist.append(dictchid)
        map = math.ceil(len(log.objects.filter(
            Q(logname__icontains=q) | Q(userid__icontains=q) | Q(content__icontains=q))) / pagesize)
        return HttpResponse(json.dumps({"mo": Modellist,"map":map}), content_type="application/json")
    else:
        return HttpResponseRedirect("index")

@login_required
def Uses(request):
    if request.user.is_superuser:
        logprint.loge("查看用户".encode("utf-8"), request.user.username, "", "query")
        return render(request, 'polls/User.html')
    else:
        return render(request, 'polls/Channel.html')



@login_required
def index(request):
    Cabsize = Cable.objects.all().count()
    Fsize = Fibre.objects.all().count()
    Chsize = Channel.objects.all().count()
    Crsize = ChanelRoute.objects.all().count()
    logsizse=log.objects.all().order_by("-pk")[:8]

    return render(request, 'polls/admin-index.html',{"Fibe":Fsize,"Channel":Chsize,"ChR":Crsize,"Cab":Cabsize,"log":logsizse })

@login_required
def setting(request):
    cont={"name":request.user.username}
    return render(request, 'polls/setting.html',cont)


@login_required
def loadd(request):
    return render(request, 'polls/load.html')


@login_required
def loachanel(request):
    return render(request, 'polls/loachanel.html')


@login_required
def cabload(request):
    return render(request, 'polls/loadcab.html')
@login_required
def wsrload(request):
    return render(request, 'polls/loaclwsr.html')


@login_required
def add(request):
    return render(request, 'polls/add.html')


@login_required
def chadd(request):
    return render(request, 'polls/chadd.html')


@login_required
def cabadd(request):
    return render(request, 'polls/cabadd.html')


@login_required
def Show(request):
    name = request.GET.get('id')
    Chall = Fibre.objects.filter(FibreName=name)
    lis = []
    fis = []
    num = 0
    if Chall:

        for fire in Chall:
            dictchid = {}
            dictchid['FibreName'] = fire.FibreName
            dictchid['Cable'] = fire.Cable
            dictchid['Acap'] = fire.Acap
            dictchid['Bcap'] = fire.Bcap
            dictchid['Aposition'] = fire.Aposition
            dictchid['Bposition'] = fire.Bposition
            dictchid['Aport'] = fire.Aport
            dictchid['Bport'] = fire.Bport
            dictchid['MainMan'] = fire.MainMan
            dictchid['BkMan'] = fire.BkMan
            fibes = fire.channel_set.all()
            use = fire.channel_set.filter(STATE="已使用")
            no = fire.channel_set.filter(STATE="未分配")
            error = fire.channel_set.filter(STATE="故障")
            num = len(fibes)
            for fb in fibes:
                fbch = {}
                fbch['Channelname'] = fb.Channelname
                fis.append(fbch)
            dictchid['StartData'] = fire.StartData
            lis.append(dictchid)
        print(num)
        return render(request, 'polls/Showw.html',
                      {"name": lis, "num": num, "fibes": fis, 'cabid': name, 'use': len(use), 'no': len(no),
                       'error': len(error)})


@login_required
def CabShow(request):
    name = request.GET.get('id')
    ca = Cable.objects.filter(Cablename=name)
    num = 0
    lis = []
    fis = []
    contxr = {"name": lis}
    if ca:
        for fire in ca:
            dictchid = {}

            dictchid['Cablename'] = fire.Cablename
            dictchid['Sup'] = fire.Sup
            dictchid['Apoint'] = fire.Apoint
            dictchid['Bpoint'] = fire.Bpoint
            dictchid['FinshDate'] = fire.FinshDate
            dictchid['Distance'] = fire.Distance
            dictchid['MainMan'] = fire.MainMan
            dictchid['BkMan'] = fire.BkMan
            dictchid['Corenumber'] = fire.Corenumber
            dictchid['Contractnumber'] = fire.Contractnumber
            dictchid['BusinessMan'] = fire.BusinessMan
            dictchid['ProtectMan'] = fire.ProtectMan
            fibes = fire.fibre_set.all()
            use = fire.fibre_set.filter(STATE="已使用")
            no = fire.fibre_set.filter(STATE="未分配")
            error = fire.fibre_set.filter(STATE="故障")
            num = len(fibes)
            for fb in fibes:
                fbch = {}

                fbch['FibreName'] = fb.FibreName
                fis.append(fbch)
            lis.append(dictchid)
        return render(request, 'polls/ShowwCab.html',
                      {"name": lis, "num": num, "fibes": fis, 'cabid': name, 'use': len(use), 'no': len(no),
                       'error': len(error)})


@login_required
def ChShow(request):
    name = request.GET.get('id')
    Chall = Channel.objects.filter(Channelname=name)
    lis = []
    Fibes = []
    if Chall:
        Map = Chall[0].Firbes.all()
        for m in Map:
            Fibes.append(m.FibreName)
        for fire in Chall:
            dictchid = {}
            dictchid['Channelname'] = fire.Channelname
            dictchid['Firbenumber'] = fire.Firbenumber
            dictchid['Acap'] = fire.Acap
            dictchid['Bcap'] = fire.Bcap
            dictchid['Business'] = fire.Business
            dictchid['Customer'] = fire.Customer
            dictchid['Aposition'] = fire.Aposition
            dictchid['Bposition'] = fire.Bposition
            dictchid['AChannel'] = fire.AChannel
            dictchid['BChannel'] = fire.BChannel
            dictchid['Mainman'] = fire.Mainman
            dictchid['BkMan'] = fire.BkMan
            dictchid['Aequipment'] = fire.Aequipment
            dictchid['Bequipment'] = fire.Bequipment
            dictchid['Aassets'] = fire.Aassets
            dictchid['Bassets'] = fire.Bassets
            lis.append(dictchid)
        contxr = {"name": lis, "Fibes": Fibes}
        return render(request, 'polls/ShowwChannel.html', contxr)

@login_required
def WsrShow(request):
    name = request.GET.get('id')
    Chall = ChanelRoute.objects.filter(ChanelRouteNumber=name)
    lis = []
    Channel = []
    Fibes = set()
    if Chall:
        Map = Chall[0].ChanelNumber.all()
        for m in Map:
            Channel.append(m.Channelname)
            for fibe in m.Firbes.all():
                Fibes.add(fibe.FibreName)
        for fire in Chall:
            dictchid = {}
            dictchid['Channelname'] = fire.ChanelRouteNumber
            dictchid['Business'] = fire.Business
            dictchid['Customer'] = fire.Customer
            dictchid['Mainman'] = fire.Mainman
            dictchid['BkMan'] = fire.BkMan
            lis.append(dictchid)
        contxr = {"name": lis, "Fibes": Fibes, "Channel": Channel}
        return render(request, 'polls/ShowwWsr.html', contxr)
