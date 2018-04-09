import re
import os
from io import StringIO

import time
import xlrd
from django.contrib.auth.models import User
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from xlwt import Workbook

from adc import logprint
from star.settings import BASE_DIR
from adc.models import Cable, Fibre, Channel, ChanelRoute, log


def Save(request, name):
    workbook = xlrd.open_workbook(BASE_DIR + name)
    table = workbook.sheet_by_index(0)
    nrows = table.nrows
    ErrorList = []
    x = y = z = 0
    ncols = table.ncols

    for x in range(1, nrows):
        row = table.row_values(x)
        for y in range(0, ncols):
            if type(row[y]) == float:
                row[y] = int(row[y])
        if row[1] == '':
            if row[0] == "添加":
                if Fibre.objects.filter(FibreName=row[3].strip()).exists():
                    error = '添加的第' + str(x) + "行已经存在!"
                    ErrorList.append(error)
                else:
                    if Cable.objects.filter(Cablename=row[2].strip()):
                        fb = Fibre(FibreName=row[3].strip(), Acap=row[4].strip(), Aposition=row[5].strip(),
                                   Aport=row[6].strip(), Bcap=row[7].strip(),
                                   Bposition=row[8].strip(), Bport=row[9].strip(), MainMan=row[10].strip(),
                                   BkMan=row[11].strip(), StartData=row[12], STATE=row[13])
                        ca = Cable.objects.filter(Cablename=row[2].strip())
                        fb.Cable = ca[0]
                        fb.save()

            if row[0] == "删除":
                if Fibre.objects.filter(FibreName=row[3].strip()).exists():
                    Fb = Fibre.objects.filter(FibreName=row[3].strip())
                    Fb.delete()
                else:
                    error = '删除的第' + str(x) + "行不存在!"
                    ErrorList.append(error)
            if row[0] == "修改":
                if Fibre.objects.filter(FibreName=row[3].strip()).exists():
                    if Cable.objects.filter(Cablename=row[2].strip()):
                        Fb = Fibre.objects.filter(FibreName=row[3].strip())
                        Fb.update(FibreName=row[3].strip(), Acap=row[4].strip(),
                                  Aposition=row[5].strip(), Aport=row[6].strip(), Bcap=row[7].strip(),
                                  Bposition=row[8].strip(), Bport=row[9].strip(), MainMan=row[10].strip(),
                                  BkMan=row[11].strip(), StartData=row[12], STATE=row[13])
                        ca = Cable.objects.filter(Cablename=row[2].strip())
                        fb.Cable = ca[0]
                        fb.save()
                    else:
                        error = '修改的第' + str(x) + "行光缆不存在!"
                        ErrorList.append(error)
                else:
                    error = '修改的第' + str(x) + "行不存在!"
                    ErrorList.append(error)
        else:
            if Fibre.objects.filter(FibreName=row[1]).exists() and Fibre.objects.filter(
                    FibreName=row[3]).exists() != True:
                Fb = Fibre.objects.filter(FibreName=row[1])
                Fb.update(Cable=row[2].strip(), FibreName=row[3].strip(), Acap=row[4].strip(), Aposition=row[5].strip(),
                          Aport=row[6].strip(), Bcap=row[7].strip(),
                          Bposition=row[8].strip(), Bport=row[9].strip(), MainMan=row[10].strip(),
                          BkMan=row[11].strip(), StartData=row[12], STATE=row[13])
            else:
                error = '第' + str(x) + "行旧编号不存在或者新编号已存在!"
                ErrorList.append(error)

        y = y + 1
    return ErrorList


def SaveChannel(request, name):
    workbook = xlrd.open_workbook(BASE_DIR + name)
    table = workbook.sheet_by_index(0)
    nrows = table.nrows
    ErrorList = []
    x = y = z = 0
    ncols = table.ncols

    for x in range(1, nrows):
        row = table.row_values(x)
        opera = True
        for y in range(0, ncols):
            if type(row[y]) == float:
                row[y] = int(row[y])
        if row[1] == '':
            if row[0] == "添加":
                if Channel.objects.filter(Channelname=row[5]).exists():
                    error = '添加的第' + str(x) + "行已经存在!"
                    ErrorList.append(error)
                else:
                    rex = row[4].strip()
                    sum = re.split(r'[/:|\n]', rex)
                    tl = True
                    for sx in sum:
                        fls = Fibre.objects.filter(FibreName=sx.strip())
                        if fls:
                            pass
                        else:
                            tl = False
                            error = '添加的第' + str(x) + "行光纤不存在!"
                            ErrorList.append(error)
                            break
                    if tl:
                        CHa = Channel(Business=row[2].strip(), Customer=row[3].strip(), Firbenumber=row[4].strip(),
                                      Channelname=row[5].strip(), CORE=row[6], TYPE=row[7], Acap=row[8],
                                      Bcap=row[9],
                                      Aposition=row[10],
                                      Bposition=row[11], Aequipment=row[12], Bequipment=row[13],
                                      AChannel=row[14], BChannel=row[15],
                                      Aassets=row[16], Bassets=row[17], STATE=row[18].strip(), Mainman=row[19].strip(),
                                      BkMan=row[20].strip())
                        CHa.save()
                        for sx in sum:
                            fls = Fibre.objects.get(FibreName=sx.strip())
                            CHa.Firbes.add(fls)

            if row[0] == "删除":
                if Channel.objects.filter(Channelname=row[5].strip()).exists():
                    Fb = Channel.objects.filter(Channelname=row[5].strip())
                    Fb.delete()
                else:
                    error = '删除第' + str(x) + "行不存在!"
                    ErrorList.append(error)

            if row[0] == "修改":
                if Channel.objects.filter(Channelname=row[5].strip()).exists():
                    rex = row[4].strip()
                    sum = re.split(r'[/:|\n]', rex)
                    tl=True
                    for sx in sum:
                        fls=Fibre.objects.filter(FibreName=sx.strip())
                        if fls:
                            pass
                        else:
                            tl=False
                            error = '修改的第' + str(x) + "行光纤不存在!"
                            ErrorList.append(error)
                            break
                    if tl:

                        Fb = Channel.objects.filter(Channelname=row[5].strip())
                        Fb.update(Business=row[2].strip(), Customer=row[3].strip(), Firbenumber=row[4].strip(),
                                  Channelname=row[5].strip(), CORE=row[6], TYPE=row[7], Acap=row[8],
                                  Bcap=row[9],
                                  Aposition=row[10],
                                  Bposition=row[11], Aequipment=row[12], Bequipment=row[13],
                                  AChannel=row[14], BChannel=row[15],
                                  Aassets=row[16], Bassets=row[17], STATE=row[18].strip(), Mainman=row[19].strip(),
                                  BkMan=row[20].strip())
                        for sx in sum:
                            fls = Fibre.objects.get(FibreName=sx.strip())
                            Fb[0].Firbes.add(fls)
                    else:
                       pass

                else:
                    error = '修改第' + str(x) + "行波道不存在!"
                    ErrorList.append(error)
        else:
            if Channel.objects.filter(Channelname=row[1].strip()).exists() and Channel.objects.filter(
                    Channelname=row[5]).exists() != True:
                Fb = Channel.objects.filter(Channelname=row[1].strip())
                Fb.update(Business=row[2].strip(), Customer=row[3].strip(), Firbenumber=row[4].strip(),
                          Channelname=row[5].strip(), Acap=row[6],
                          Bcap=row[7],
                          Aposition=row[8],
                          Bposition=row[9], Aequipment=row[10].strip(), Bequipment=row[11].strip(),
                          AChannel=row[12], BChannel=row[13],
                          Aassets=row[14].strip(), Bassets=row[15].strip(), Mainman=row[16].strip(),
                          BkMan=row[17].strip())
            else:
                error = '第' + str(x) + "行旧编号不存在或者新编号已存在!"
                ErrorList.append(error)
        y = y + 1

    return ErrorList


def SaveCab(request, name):
    workbook = xlrd.open_workbook(BASE_DIR + name)
    table = workbook.sheet_by_index(0)
    nrows = table.nrows
    ErrorList = []
    x = y = z = 0
    ncols = table.ncols
    for x in range(1, nrows):
        row = table.row_values(x)
        for y in range(0, ncols):
            if type(row[y]) == float:
                row[y] = int(row[y])
        if row[1] == '':
            if row[0] == "添加":
                if Cable.objects.filter(Cablename=row[2].strip()).exists():
                    error = '添加的第' + str(x) + "行已经存在!"
                    ErrorList.append(error)
                else:
                    Cable(Cablename=row[2].strip(), Sup=row[3].strip(), Apoint=row[4].strip(), Apointadd=row[5].strip(),
                          Bpoint=row[6].strip(), Bpointadd=row[7].strip(),
                          BusinessMan=row[8].strip(), ProtectMan=row[9].strip(), FinshDate=row[10],
                          Distance=row[11], Corenumber=row[12], Contractnumber=row[13], BkMan=row[15],
                          To=row[16], MainMan=row[14]).save()

            if row[0] == "删除":
                if Cable.objects.filter(Cablename=row[2].strip()).exists():
                    try:
                        Fb = Cable.objects.filter(Cablename=row[2].strip())
                        if Fb[0].fibre_set.all().count()!=0:
                            error = '删除的第' + str(x) + "行有子数据存在,请先删除子数据!"
                            ErrorList.append(error)
                        else:
                            Fb.delete()
                    except error:
                        print("ccccc")
                else:
                    error = '删除的第' + str(x) + "行不存在!"
                    ErrorList.append(error)
            if row[0] == "修改":
                if Cable.objects.filter(Cablename=row[2].strip()).exists():
                    Fb = Cable.objects.filter(Cablename=row[2].strip())
                    Fb.update(Cablename=row[2].strip(), Sup=row[3].strip(), Apoint=row[4].strip(),
                              Apointadd=row[5].strip(),
                              Bpoint=row[6].strip(), Bpointadd=row[7].strip(),
                              BusinessMan=row[8].strip(), ProtectMan=row[9].strip(), FinshDate=row[10],
                              Distance=row[11], Corenumber=row[12], Contractnumber=row[13], BkMan=row[15],
                              To=row[16], MainMan=row[14])
                else:
                    error = '修改的第' + str(x) + "行不存在!"
                    ErrorList.append(error)
        else:
            if Cable.objects.filter(Cablename=row[1]).exists() and Cable.objects.filter(
                    Cablename=row[2]).exists() != True:
                Fb = Cable.objects.filter(Cablename=row[1])
                Fb.update(Cablename=row[2].strip(), Sup=row[3].strip(), Apoint=row[4].strip(), Apointadd=row[5].strip(),
                          Bpoint=row[6].strip(), Bpointadd=row[7].strip(),
                          BusinessMan=row[8].strip(), ProtectMan=row[9].strip(), FinshDate=row[10],
                          Distance=row[11], Corenumber=row[12], Contractnumber=row[13], BkMan=row[15],
                          To=row[16], MainMan=row[14])
            else:
                error = '第' + str(x) + "行旧编号不存在或者新编号已存在!"
                ErrorList.append(error)

        y = y + 1
    return ErrorList


def SaveWsr(request, name):
    workbook = xlrd.open_workbook(BASE_DIR + name)
    table = workbook.sheet_by_index(0)
    nrows = table.nrows
    ErrorList = []
    x = y = z = 0
    ncols = table.ncols
    for x in range(1, nrows):
        row = table.row_values(x)
        for y in range(0, ncols):
            if type(row[y]) == float:
                row[y] = int(row[y])
        if row[1] == '':
            if row[0] == "添加":
                rex = row[5].strip()
                sum = re.split(r'[/]', rex)
                if ChanelRoute.objects.filter(ChanelRouteNumber=row[4].strip()).exists():
                    error = '添加的第' + str(x) + "行已经存在!"
                    ErrorList.append(error)
                else:
                    Chanr = ChanelRoute(Business=row[2].strip(), Customer=row[3].strip(),
                                        ChanelRouteNumber=row[4].strip(), ChanelNumbers=row[5].strip())
                    Chanr.save()
                    bl = True
                    for sm in sum:
                        fibe = Channel.objects.filter(Channelname=sm.strip())
                        if fibe:
                            pass
                        else:
                            error = '添加的第' + str(x) + "行不存在!"
                            ErrorList.append(error)
                            bl = False
                            break
                    if bl:
                        for sm in sum:
                            cc = Channel.objects.filter(Channelname=sm.strip())
                            cc[0].chanelroute_set.add(Chanr)
                    else:
                        Chanr.delete()
            if row[0] == "删除":
                try:
                    cha = ChanelRoute.objects.get(ChanelRouteNumber=row[4].strip())

                    if cha:
                        cha.ChanelNumber.clear
                        cha.delete()
                    else:
                        error = '删除的第' + str(x) + "行不存在!"
                        ErrorList.append(error)
                except ObjectDoesNotExist:
                    error = '删除的第' + str(x) + "行不存在!"
                    ErrorList.append(error)

            if row[0] == "修改":
                cha = ChanelRoute.objects.filter(ChanelRouteNumber=row[4].strip())
                if cha:
                    rex = row[5].strip()
                    sum = re.split(r'[/]', rex)
                    bl = True
                    for sm in sum:
                        fibe = Channel.objects.filter(Channelname=sm.strip())
                        if fibe:
                            pass
                        else:
                            error = '修改的第' + str(x) + "行波道不存在!"
                            ErrorList.append(error)
                            bl = False
                            break
                    if bl:
                        for sm in sum:
                            cc = Channel.objects.filter(Channelname=sm.strip())
                            cc.chanelroute_set.add(cha)
                        cha.update(Business=row[2].strip(), Customer=row[3].strip())

                else:
                    error = '修改的第' + str(x) + "行不存在!"
                    ErrorList.append(error)
        else:
            if ChanelRoute.objects.filter(Cablename=row[1]).exists() and Cable.objects.filter(
                    Cablename=row[2]).exists() != True:
                Fb = ChanelRoute.objects.filter(Cablename=row[1])
                Fb.update(Cablename=row[2].strip(), Sup=row[3].strip(), Apoint=row[4].strip(), Apointadd=row[5].strip(),
                          Bpoint=row[6].strip(), Bpointadd=row[7].strip(),
                          BusinessMan=row[8].strip(), ProtectMan=row[9].strip(), FinshDate=row[10],
                          Distance=row[11], Corenumber=row[12], Contractnumber=row[13], BkMan=row[15],
                          To=row[16], MainMan=row[14])
            else:
                error = '第' + str(x) + "行旧编号不存在或者新编号已存在!"
                ErrorList.append(error)

        y = y + 1
    return ErrorList


def update(request):
    name = request.GET.get('id')
    Chall = Fibre.objects.filter(FibreName=name)
    lis = []
    use = ""
    no = ""
    error = ""

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
            dictchid['StartData'] = fire.StartData
            dictchid['STATE'] = fire.STATE
            lis.append(dictchid)
        return render(request, 'polls/update.html', {"name": lis, "use": use})


def chupdate(request):
    name = request.GET.get('id')
    Chall = Channel.objects.filter(Channelname=name)
    fibelist = set()
    lis = []
    if Chall:
        for fire in Chall:
            dictchid = {}
            dictchid['Channelname'] = fire.Channelname
            dictchid['Firbenumber'] = fire.Firbenumber
            dictchid['Acap'] = fire.Acap
            dictchid['Bcap'] = fire.Bcap
            dictchid['Business'] = fire.Business
            for fibe in fire.Firbes.all():
                fibelist.add(fibe.FibreName)
            dictchid['Customer'] = fire.Customer
            dictchid['Aposition'] = fire.Aposition
            dictchid['Bposition'] = fire.Bposition
            dictchid['TYPE'] = fire.TYPE
            dictchid['CORE'] = fire.CORE
            dictchid['STATE'] = fire.STATE
            dictchid['AChannel'] = fire.AChannel
            dictchid['BChannel'] = fire.BChannel
            dictchid['Mainman'] = fire.Mainman
            dictchid['BkMan'] = fire.BkMan
            dictchid['Aequipment'] = fire.Aequipment
            dictchid['Bequipment'] = fire.Bequipment
            dictchid['Aassets'] = fire.Aassets
            dictchid['Bassets'] = fire.Bassets
            lis.append(dictchid)
        contxr = {"name": lis, "list": fibelist}
        return render(request, 'polls/updateChannel.html', contxr)


def wsrupdate(request):
    name = request.GET.get('id')
    Chall = ChanelRoute.objects.filter(ChanelRouteNumber=name)
    fibelist = set()
    lis = []
    if Chall:
        for fire in Chall:
            dictchid = {}
            dictchid['Business'] = fire.Business
            for fibe in fire.ChanelNumber.all():
                fibelist.add(fibe.Channelname)
            dictchid['Customer'] = fire.Customer
            dictchid['ChanelRouteNumber'] = fire.ChanelRouteNumber
            dictchid['BkMan'] = fire.BkMan
            lis.append(dictchid)
        contxr = {"name": lis, "list": fibelist}
        return render(request, 'polls/updatewsr.html', contxr)


def cabupdate(request):
    name = request.GET.get('id')
    ca = Cable.objects.filter(Cablename=name)
    lis = []
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

            lis.append(dictchid)

        return render(request, 'polls/updateCab.html', contxr)


def userupdate(request):
    name = request.GET.get('id')
    ca = User.objects.get(username=name)
    lis = []
    contxr = {"name": lis}
    dictchid = {}
    dictchid['username'] = ca.username
    lis.append(dictchid)
    return render(request, 'polls/userudpe.html', contxr)


def deletfirbe(request):
    name = request.GET.get('id')
    fibre = Fibre.objects.filter(FibreName=name)
    fibre[0].delete()
    resp = {'code': 100, 'detail': 'Get success'}
    logprint.loge("删除光纤", request.user.username, "编号"+name, "deleteFibe")
    return HttpResponse(json.dumps(resp), content_type="application/json")


def chdeletfirbe(request):
    name = request.GET.get('id')
    fibre = Channel.objects.filter(Channelname=name)
    fibre.delete()
    resp = {'code': 100, 'detail': 'Get success'}
    logprint.loge("删除波道", request.user.username, "编号"+name, "deleteCh")
    return HttpResponse(json.dumps(resp), content_type="application/json")


def cabdeletfirbe(request):
    name = request.GET.get('id')
    fibre = Cable.objects.filter(Cablename=name)
    fibre.delete()
    resp = {'code': 100, 'detail': 'Get success'}
    logprint.loge("删除光缆", request.user.username, "编号"+name, "deleteCab")
    return HttpResponse(json.dumps(resp), content_type="application/json")


def Wetfirbe(request):
    name = request.GET.get('id')
    fibre = ChanelRoute.objects.get(ChanelRouteNumber=name)
    fibre.ChanelNumber.clear
    fibre.delete()
    resp = {'code': 100, 'detail': 'Get success'}
    logprint.loge("删除波道路由", request.user.username, "编号"+name, "deleteWsr")
    return HttpResponse(json.dumps(resp), content_type="application/json")

def deluser(request):
    name = request.GET.get('id')
    fibre = User.objects.get(username=name)
    fibre.delete()
    resp = {'code': 100, 'detail': 'Get success'}
    logprint.loge("删除用户", request.user.username, "用户名"+name, "deleteUser")
    return HttpResponse(json.dumps(resp), content_type="application/json")


def addfibre(request):
    fbname = request.POST.get('fbname')
    cabname = request.POST.get('cab')
    acap = request.POST.get('acap')
    bcap = request.POST.get('bcap')
    apos = request.POST.get('apos')
    bpos = request.POST.get('bpos')
    aport = request.POST.get('aport')
    bport = request.POST.get('bport')
    man = request.POST.get('man')
    bk = request.POST.get('bk')
    date = request.POST.get('date')
    if Fibre.objects.filter(FibreName=fbname).exists():
        return render(request, 'polls/error.html')
    else:
        fibre = Fibre(Cable=cabname, FibreName=fbname, Acap=acap, Aposition=apos, Aport=aport, Bcap=bcap,
                      Bposition=bpos, Bport=bport, MainMan=man, BkMan=bk, StartData=date)
        fibre.save()
        return render(request, 'polls/ko.html')


def usadd(request):

    return render(request, 'polls/adduser.html')



def delog(request):
    log.objects.all().delete()
    return HttpResponse(json.dumps({"data":10}), content_type="application/json")



def addch(request):

    newname = request.POST.get('Channelname')
    Firbenumber = request.POST.get('Firbenumber')
    acap = request.POST.get('acap')
    bcap = request.POST.get('bcap')
    apos = request.POST.get('apos')
    bpos = request.POST.get('bpos')
    man = request.POST.get('man')
    AChannel = request.POST.get('AChannel')
    BChannel = request.POST.get('BChannel')
    Aequipment = request.POST.get('Aequipment')
    Bequipment = request.POST.get('Bequipment')
    Aassets = request.POST.get('Aassets')
    Bassets = request.POST.get('Bassets')
    Business = request.POST.get('Business')
    Customer = request.POST.get('Customer')
    bk = request.POST.get('bk')
    if Channel.objects.filter(Channelname=newname).exists():
        return render(request, 'polls/error.html')
    else:
        Channel(Business=Business.strip(), Customer=Customer.strip(), Firbenumber=Firbenumber.strip(),
                Channelname=newname.strip(), Acap=acap,
                Bcap=bcap,
                Aposition=apos,
                Bposition=bpos, Aequipment=Aequipment, Bequipment=Bequipment,
                AChannel=AChannel, BChannel=BChannel,
                Aassets=Aassets, Bassets=Bassets, Mainman=man,
                BkMan=bk.strip()).save()
        return render(request, 'polls/ko.html')

def daochu(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=beifen' + time.strftime('%Y%m%d', time.localtime(
        time.time())) + '.xls'
    list_obj = log.objects.all().order_by("-pk")
    if list_obj:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表第一页")
        w.write(0, 0, "id")
        w.write(0, 1, u"操作")
        w.write(0, 2, u"时间")
        w.write(0, 3, u"用户")
        w.write(0, 4, u"信息")
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            data_id = obj.id
            data_logname = obj.logname
            data_time = obj.Credate.strftime("%Y-%m-%d")
            data_userid = obj.userid
            data_content = obj.content
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_logname)
            w.write(excel_row, 2, data_time)
            w.write(excel_row, 3, data_userid)
            w.write(excel_row, 4, data_content)
            excel_row += 1
        ws.save(response)
        return response
def Chdaochu(request):
    if Channel.objects.all().count()!=0:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=波道数据' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        list_obj = Channel.objects.all().order_by("-pk")
        if list_obj:
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "id")
            w.write(0, 1, u"业务")
            w.write(0, 2, u"客户")
            w.write(0, 3, u"光纤编号")
            w.write(0, 4, u"波道编号")
            w.write(0, 5, u"多芯")
            w.write(0, 6, u"波道类型")
            w.write(0, 7, u"A端机柜")
            w.write(0, 8, u"B端机柜")
            w.write(0, 9, u"A端机位")
            w.write(0, 10, u"B端机位")
            w.write(0, 11, u"A端设备")
            w.write(0, 12, u"B端设备")
            w.write(0, 13, u"A端波道")
            w.write(0, 14, u"B端波道")
            w.write(0, 15, u"A端资产编号")
            w.write(0, 16, u"B端资产编号")
            w.write(0, 17, u"状态")
            w.write(0, 18, u"负责人")
            w.write(0, 19, u"备份负责人")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                data_id = obj.id
                Business = obj.Business
                Customer = obj.Customer
                Firbenumber = obj.Firbenumber
                Channelname = obj.Channelname
                CORE = obj.CORE
                TYPE = obj.TYPE
                Acap = obj.Acap
                Bcap = obj.Bcap
                Aposition = obj.Aposition
                Bposition = obj.Bposition
                Aequipment = obj.Aequipment
                Bequipment = obj.Bequipment
                AChannel = obj.AChannel
                BChannel = obj.BChannel
                Aassets = obj.Aassets
                Bassets = obj.Bassets
                STATE = obj.STATE
                Mainman = obj.Mainman
                BkMan = obj.BkMan
                w.write(excel_row, 0, data_id)
                w.write(excel_row, 1, Business)
                w.write(excel_row, 2, Customer)
                w.write(excel_row, 3, Firbenumber)
                w.write(excel_row, 4, Channelname)
                w.write(excel_row, 5, CORE)
                w.write(excel_row, 6, TYPE)
                w.write(excel_row, 7, Acap)
                w.write(excel_row, 8, Bcap)
                w.write(excel_row, 9, Aposition)
                w.write(excel_row, 10, Bposition)
                w.write(excel_row, 11, Aequipment)
                w.write(excel_row, 12, Bequipment)
                w.write(excel_row, 13, AChannel)
                w.write(excel_row, 14, BChannel)
                w.write(excel_row, 15, Aassets)
                w.write(excel_row, 16, Bassets)
                w.write(excel_row, 17, STATE)
                w.write(excel_row, 18, Mainman)
                w.write(excel_row, 19, BkMan)
                excel_row += 1
            ws.save(response)
            return response
    else:
        return HttpResponseRedirect("Channel")
def Fiechu(request):
    if Fibre.objects.all().count()!=0:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=光纤数据' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        list_obj = Fibre.objects.all().order_by("-pk")
        if list_obj:
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "id")
            w.write(0, 1, u"光缆")
            w.write(0, 2, u"光纤编号")
            w.write(0, 3, u"A端机柜")
            w.write(0, 4, u"A端机位")
            w.write(0, 5, u"A端端子")
            w.write(0, 6, u"B端机柜")
            w.write(0, 7, u"B端机位")
            w.write(0, 8, u"B端端子")
            w.write(0, 9, u"负责人")
            w.write(0, 10, u"备份负责人")
            w.write(0, 11, u"分配时间")
            w.write(0, 12, u"状态")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                data_id = obj.id
                Cable = obj.Cable.Cablename
                FibreName = obj.FibreName
                Acap = obj.Acap
                Aposition = obj.Aposition
                Aport = obj.Aport
                Bcap = obj.Bcap
                Bposition = obj.Bposition
                Bport = obj.Bport
                MainMan = obj.MainMan
                BkMan = obj.BkMan
                StartData = obj.StartData
                STATE = obj.STATE
                w.write(excel_row, 0, data_id)
                w.write(excel_row, 1, Cable)
                w.write(excel_row, 2, FibreName)
                w.write(excel_row, 3, Acap)
                w.write(excel_row, 4, Aposition)
                w.write(excel_row, 5, Aport)
                w.write(excel_row, 6, Bcap)
                w.write(excel_row, 7, Bposition)
                w.write(excel_row, 8, Bport)
                w.write(excel_row, 9, MainMan)
                w.write(excel_row, 10, BkMan)
                w.write(excel_row, 11, StartData)
                w.write(excel_row, 12, STATE)
                excel_row += 1
            ws.save(response)
            return response
    else:
        return HttpResponseRedirect("Fibe")
def cadao(request):
    if Cable.objects.all().count()!=0:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=光缆数据' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        list_obj = Cable.objects.all().order_by("Cablename")
        if list_obj:
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "id")
            w.write(0, 1, u"光缆编号")
            w.write(0, 2, u"供应商")
            w.write(0, 3, u"A端")
            w.write(0, 4, u"A端地址")
            w.write(0, 5, u"B端")
            w.write(0, 6, u"B端地址")
            w.write(0, 7, u"商务对口人及电话")
            w.write(0, 8, u"维护联系人及电话")
            w.write(0, 9, u"完工时间")
            w.write(0, 10, u"距离")
            w.write(0, 11, u"芯数")
            w.write(0, 12, u"合同编号")
            w.write(0, 13, u"负责人")
            w.write(0, 14, u"备份负责人")
            w.write(0, 15, u"所属地")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                data_id = obj.id
                Cablename = obj.Cablename
                Sup = obj.Sup
                Apoint = obj.Apoint
                Apointadd = obj.Apointadd
                Bpoint = obj.Bpoint
                Bpointadd = obj.Bpointadd
                BusinessMan = obj.BusinessMan
                ProtectMan = obj.ProtectMan
                FinshDate = obj.FinshDate
                Distance = obj.Distance
                Corenumber = obj.Corenumber
                Contractnumber = obj.Contractnumber
                MainMan = obj.MainMan
                BkMan = obj.BkMan
                To = obj.To
                w.write(excel_row, 0, data_id)
                w.write(excel_row, 1, Cablename)
                w.write(excel_row, 2, Sup)
                w.write(excel_row, 3, Apoint)
                w.write(excel_row, 4, Apointadd)
                w.write(excel_row, 5, Bpoint)
                w.write(excel_row, 6, Bpointadd)
                w.write(excel_row, 7, BusinessMan)
                w.write(excel_row, 8, ProtectMan)
                w.write(excel_row, 9, FinshDate)
                w.write(excel_row, 10, Distance)
                w.write(excel_row, 11, Corenumber)
                w.write(excel_row, 12, Contractnumber)
                w.write(excel_row, 13, MainMan)
                w.write(excel_row, 14, BkMan)
                w.write(excel_row, 15, To)
                excel_row += 1
            ws.save(response)
            return response
    return HttpResponseRedirect("Cable")
def bodao(request):
    if ChanelRoute.objects.all().count()!=0:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=波道路由数据' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        list_obj = ChanelRoute.objects.all().order_by("ChanelRouteNumber")
        if list_obj:
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "id")
            w.write(0, 1, u"业务")
            w.write(0, 2, u"客户")
            w.write(0, 3, u"路由编号")
            w.write(0, 4, u"波道编号")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                data_id = obj.id
                Business = obj.Business
                Customer = obj.Customer
                ChanelRouteNumber = obj.ChanelRouteNumber
                st=""
                for sx in obj.ChanelNumber.all():
                    st=sx.Channelname+"/"+st
                st =st

                w.write(excel_row, 0, data_id)
                w.write(excel_row, 1, Business)
                w.write(excel_row, 2, Customer)
                w.write(excel_row, 3, ChanelRouteNumber)
                w.write(excel_row, 4, st)
                excel_row += 1
            ws.save(response)
            return response
    else:
        return HttpResponseRedirect("Wsr")