import json
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
import math
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

from adc import logprint
from adc.models import Fibre, Channel, Cable, ChanelRoute, log

def Queryfirbe(request):
    page = int(request.GET.get('page', 1))
    pagesize = int(request.GET.get('pagesize', 10))
    fire = request.GET.get('firenumber')
    pro = request.GET.get('protect')
    cab = request.GET.get('cab')
    state = request.GET.get('state')
    querydict = {}

    # 条件搜索区域
    if fire:
        # 单个查询条件
        querydict['FibreName__icontains'] = fire
    if pro:
        querydict['MainMan__icontains'] = pro
    if cab:
        querydict['Cable__Cablename__icontains'] = cab
    if state:
        querydict['STATE__icontains'] = state

    # 获得总页数
    size = math.ceil(len(Fibre.objects.filter(**querydict)) / pagesize)
    # 准备一个列表
    Modellist = []
    # 分页查询结果集
    result = Fibre.objects.filter(**querydict)[(page - 1) * pagesize:page * pagesize]
    if result:
        # 遍历结果
        for fix in result:
            dictchid = {}
            # 把结果封装到字典里
            dictchid['FibreName'] = fix.FibreName
            dictchid['Cable'] = fix.Cable.Cablename
            dictchid['MainMan'] = fix.MainMan
            dictchid['StartData'] = fix.StartData
            dictchid['STATE'] = fix.STATE
            dictchid['map'] = size
            Modellist.append(dictchid)
        logprint.loge("光纤查询",request.user.username,"成功查询","query")
        return HttpResponse(json.dumps(Modellist), content_type="application/json")
    else:
        dictchid = {}
        dictchid['FibreName'] = "未找到"
        dictchid['Cable'] = "未找到"
        dictchid['MainMan'] = "未找到"
        dictchid['StartData'] = "未找到"

        Modellist.append(dictchid)
        logprint.loge("光纤查询",request.user.username,"未找到","query")

        return HttpResponse(json.dumps(Modellist), content_type="application/json")

        # 查询结果集
        # 存储查询到的变量值的列表
        # 如果有查询结果


# 波道查询方法


def QureyChannel(request):
    page = int(request.GET.get('page', 1))
    pagesize = int(request.GET.get('pagesize', 10))
    channel = request.GET.get('channel')
    Firbenumber = request.GET.get('Firbenumber')
    pro = request.GET.get('pro')
    state = request.GET.get('state')
    # 查询条件字典
    querydict = {}
    # 查询条件判断
    if channel:
        querydict['Channelname__icontains'] = channel
    # 查询条件判断

    if pro:
        querydict['Mainman__icontains'] = pro
    if state:
        querydict['STATE__icontains'] = state
    if Firbenumber:
        querydict['Firbenumber__icontains'] = Firbenumber
    # 查询结果集
    result = Channel.objects.filter(**querydict).order_by("Channelname")[(page - 1) * pagesize:page * pagesize]
    # 存储查询到的变量值的列表
    Modellist = []
    # 如果有查询结果
    if result:
        map = math.ceil(len(Channel.objects.filter(**querydict)) / pagesize)
        for ResultChild in result:
            # 临时存储单个结果的字典
            dictchid = {}
            dictchid['Channelname'] = ResultChild.Channelname
            dictchid['Mainman'] = ResultChild.Mainman
            dictchid['Business'] = ResultChild.Business
            dictchid['Firbenumber'] = ResultChild.Firbenumber
            dictchid['STATE'] = ResultChild.STATE
            Modellist.append(dictchid)
        logprint.loge("波道查询",request.user.username,"OK","query")
        return HttpResponse(json.dumps({"   mo": Modellist, "map": map}), content_type="application/json")

    else:
        # 没有查到结果则返回未找到
        Errorlist = []
        dictchid = {}
        dictchid['Channelname'] = "未找到"
        dictchid['Mainman'] = "未找到"
        dictchid['Business'] = "未找到"
        dictchid['Firbenumber'] = "未找到"
        Errorlist.append(dictchid)
        logprint.loge("波道查询",request.user.username,"未找到","query")
        return HttpResponse(json.dumps({"mo":Errorlist}), content_type="application/json")


# 光缆查询方法
def QureyCab(request):
    page = int(request.GET.get('page', 1))
    pagesize = int(request.GET.get('pagesize', 5))
    cab = request.GET.get('cab')
    protect = request.GET.get('protect')
    number = request.GET.get('number')
    to = request.GET.get('to')
    # 查询条件字典
    querydict = {}
    if cab:
        querydict['Cablename__icontains'] = cab
    if protect:
        querydict['ProtectMan__icontains'] = protect
    if number:
        querydict['Corenumber__icontains'] = number
    if to:
        querydict['To__icontains'] = to

    Modellist = []
    map = math.ceil(len(Cable.objects.filter(**querydict)) / pagesize)
    result = Cable.objects.filter(**querydict).order_by("Cablename")[(page - 1) * pagesize:page * pagesize]
    if result:
        for ResultChild in result:
            # 临时存储单个结果的字典
            dictchid = {}

            dictchid['Cablename'] = ResultChild.Cablename
            dictchid['Apoint'] = ResultChild.Apoint
            dictchid['Bpoint'] = ResultChild.Bpoint
            dictchid['Sup'] = ResultChild.Sup
            dictchid['map'] = map
            dictchid['MainMan'] = ResultChild.MainMan
            dictchid['Corenumber'] = ResultChild.Corenumber
            dictchid['To'] = ResultChild.To
            dictchid['ProtectMan'] = ResultChild.ProtectMan
            Modellist.append(dictchid)
        return HttpResponse(json.dumps(Modellist), content_type="application/json")
    else:
        # 没有查到结果则返回未找到
        Errorlist = []
        dictchid = {}
        dictchid['Cablename'] = "未找到"
        dictchid['Corenumber'] = "未找到"
        dictchid['ProtectMan'] = "未找到"
        dictchid['Apoint'] = "未找到"
        dictchid['Bpoint'] = "未找到"
        dictchid['Sup'] = "未找到"
        dictchid['MainMan'] = "未找到"
        dictchid['To'] = "未找到"
        Errorlist.append(dictchid)
        return HttpResponse(json.dumps(Errorlist), content_type="application/json")
        # 查询结果集
        # 存储查询到的变量值的列表
        # 如果有查询结果


# 光缆查询方法
@login_required
def QureyWs(request):
    page = int(request.GET.get('page', 1))
    pagesize = int(request.GET.get('pagesize', 5))
    ChanelRouteNumber = request.GET.get('channelname')
    fir = request.GET.get('firenumber')
    # 查询条件字典
    querydict = {}
    if ChanelRouteNumber:
        querydict['ChanelNumber__Channelname__icontains'] = ChanelRouteNumber
    # 查询条件判断
    if fir:
        querydict['ChanelNumber__Firbes__FibreName__icontains'] = fir
    Modellist = []
    result = ChanelRoute.objects.filter(**querydict)[(page - 1) * pagesize:page * pagesize]
    if result:
        exist = []

        for ResultChild in result:
            Fibeset = set()
            chanset = set()
            if ResultChild.pk in exist:
                continue
            else:
                exist.append(ResultChild.pk)
            # 临时存储单个结果的字典
            dictchid = {}
            str = ""
            dictchid['Business'] = ResultChild.Business
            dictchid['Mainman'] = ResultChild.Mainman
            Call = ResultChild.ChanelNumber.all()
            for cv in Call:
                fall = cv.Channelname
                chanset.add(fall+"_")
            for cls in Call:
                fall = cls.Firbenumber.strip()
                if fall in Fibeset:
                    continue
                else:
                    Fibeset.add(fall)
            dictchid['ChanelRouteNumber'] = ResultChild.ChanelRouteNumber
            sccc=str.join(Fibeset)
            dictchid['FibreName'] = sccc
            dictchid['ChanelNumbers'] = "".join(chanset)
            Modellist.append(dictchid)
        map = math.ceil(len(ChanelRoute.objects.filter(**querydict))/ pagesize)
        return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
    else:
        # 没有查到结果则返回未找到
        Errorlist = []
        dictchid = {}
        dictchid['ChanelNumbers'] = "未找到"
        dictchid['Business'] = "未找到"
        dictchid['Mainman'] = "未找到"
        dictchid['ChanelRouteNumber'] = "未找到"
        Errorlist.append(dictchid)
        map =1
        logprint.loge("光缆查询",request.user.username,"失败","query")
        return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
        # 查询结果集
        # 存储查询到的变量值的列表
        # 如果有查询结果


def QureyUser(request):
    page = int(request.GET.get('page', 1))
    pagesize = int(request.GET.get('pagesize', 8))
    username = request.GET.get('username')
    # 查询条件字典
    querydict = {}
    if username:
        querydict['username__icontains'] = username
    # 查询条件判断
    Modellist = []
    result = User.objects.filter(**querydict)[(page - 1) * pagesize:page * pagesize]
    if result:
        exist = []
        for ResultChild in result:
            if ResultChild.pk in exist:
                continue
            else:
                exist.append(ResultChild.pk)
            # 临时存储单个结果的字典
            dictchid = {}
            dictchid['USERNAME'] = ResultChild.username
            dictchid['CRE'] = ResultChild.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            if ResultChild.last_login!=None:

                dictchid['LAST'] = ResultChild.last_login.strftime("%Y-%m-%d %H:%M:%S")
            else:
                dictchid['LAST'] = "未登录过"

            Modellist.append(dictchid)
        map = math.ceil(User.objects.filter(**querydict).count()/ pagesize)
        return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
    else:
        # 没有查到结果则返回未找到
        Errorlist = []
        dictchid = {}
        dictchid['username'] = "未找到"
        dictchid['CRE'] = "未找到"
        dictchid['LAST'] = "未找到"
        Errorlist.append(dictchid)
        map =0
        return HttpResponse(json.dumps({"mo": Errorlist, "map": map}), content_type="application/json")
        # 查询结果集
        # 存储查询到的变量值的列表
        # 如果有查询结果

def QueryLog(request):
    if request.user.is_superuser:
        page = int(request.GET.get('page', 1))
        pagesize = int(request.GET.get('pagesize', 8))
        logname = request.GET.get('log')
        # 查询条件字典
        querydict = {}
        if logname:
            querydict['logname__icontains'] = logname
        Modellist = []
        result = log.objects.filter(**querydict)[(page - 1) * pagesize:page * pagesize]
        if result:
            for ResultChild in result:
                # 临时存储单个结果的字典
                dictchid = {}
                dictchid['logname'] = ResultChild.logname
                dictchid['id'] = ResultChild.pk
                dictchid['Credate'] = ResultChild.Credate.strftime("%Y-%m-%d %H:%M:%S")
                dictchid['userid'] = ResultChild.userid
                dictchid['content'] = ResultChild.content
                Modellist.append(dictchid)
            map = math.ceil(len(Modellist)/ pagesize)
            return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
        else:
            # 没有查到结果则返回未找到
            Errorlist = []
            dictchid = {}
            dictchid['logname'] = "未找到"
            Errorlist.append(dictchid)
            map =1
            return HttpResponse(json.dumps({"mo": Modellist, "map": map}), content_type="application/json")
            # 查询结果集
            # 存储查询到的变量值的列表
            # 如果有查询结果
    else:
        return HttpResponseRedirect("index")