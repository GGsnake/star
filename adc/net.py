# 文件下载
import json

from django.contrib.auth.models import User

from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render

from django.views import generic
from django.utils import timezone

from adc import logprint
from adc.models import Channel, Fibre, Cable, ChanelRoute
from adc.sql import Save, SaveCab, SaveChannel, SaveWsr
from star.settings import BASE_DIR


def downFirbe(request):
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = BASE_DIR + "Fireexamp.xlsx"
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


# 文件下载
def downCab(request):
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = BASE_DIR + "Cabexamp.xlsx"
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


# 文件下载
def downChannel(request):
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = BASE_DIR + "Channelexamp.xlsx"
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response
def downwsr(request):
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = BASE_DIR + "wsr.xlsx"
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


def channelupdate(request):
    newname = request.POST.get('Channelname')
    acap = request.POST.get('acap')
    bcap = request.POST.get('bcap')
    apos = request.POST.get('Aposition')
    bpos = request.POST.get('Bposition')
    man = request.POST.get('Mainman')
    AChannel = request.POST.get('AChannel')
    BChannel = request.POST.get('BChannel')
    Aequipment = request.POST.get('Aequipment')
    Business = request.POST.get('Business')
    Bequipment = request.POST.get('Bequipment')
    Aassets = request.POST.get('Aassets')
    Bassets = request.POST.get('Bassets')
    Businesss = request.POST.get('Business')
    Customer = request.POST.get('Customer')
    bk = request.POST.get('BkMan')
    state = request.POST.get('STATE')
    if state != None:
        fibre = Channel.objects.filter(Channelname=newname)
        fibre.update(Business=Business.strip(), Customer=Customer.strip(),
                     Channelname=newname.strip(), Acap=acap,
                     Bcap=bcap,
                     Aposition=apos,
                     Bposition=bpos, Aequipment=Aequipment, Bequipment=Bequipment, AChannel=AChannel, BChannel=BChannel,
                     STATE=state,
                     Aassets=Aassets, Bassets=Bassets, Mainman=man,
                     BkMan=bk.strip())
        logprint.loge("修改波道", request.user.username, "波道:" + newname, "upadtechannel")
        return render(request, 'polls/ok.html')
    else:
        fibre = Channel.objects.filter(Channelname=newname)
        fibre.update(Business=Business.strip(), Customer=Customer.strip(),
                     Channelname=newname.strip(), Acap=acap,
                     Bcap=bcap,
                     Aposition=apos,
                     Bposition=bpos, Aequipment=Aequipment, Bequipment=Bequipment, AChannel=AChannel, BChannel=BChannel,

                     Aassets=Aassets, Bassets=Bassets, Mainman=man,
                     BkMan=bk.strip())
        logprint.loge("修改波道", request.user.username, "波道:" + newname, "upadtechannel")
        return render(request, 'polls/ok.html')


def srupdate(request):
    newname = request.POST.get('ChanelRouteNumber')
    Businesss = request.POST.get('Business')
    Customer = request.POST.get('Customer')
    fibre = ChanelRoute.objects.filter(ChanelRouteNumber=newname)
    fibre.update(Business=Businesss.strip(), Customer=Customer.strip()
                 )
    return render(request, 'polls/ok.html')


def userdate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if password!="":
        fibre = User.objects.get(username=username)
        fibre.set_password(password)
        fibre.save()
        logprint.loge("更新密码", username, "普通用户:" + username, "updateuser")
        return render(request, 'polls/ok.html')
    else:
        return render(request, 'polls/eoor.html')


def newuser(request):
    us = request.GET.get('username')
    pa = request.GET.get('password')
    admin=request.GET.get('admin')
    if len(User.objects.filter(username=us)) != 0:
        return HttpResponse(json.dumps({"yes": "用户已存在！"}), content_type="application/json")

    else:
        if admin=="true":
            user = User.objects.create_superuser(us,"1331@qq.com",pa)
            user.save()
            logprint.loge("新增用户", request.user.username, "普通用户:"+us, "adduser")
            return HttpResponse(json.dumps({"yes": "注册成功"}), content_type="application/json")
        else:
            user = User.objects.create_user(us)
            user.set_password(pa)
            user.save()
            logprint.loge("新增用户", request.user.username, "管理员:"+us, "adduser")
            return HttpResponse(json.dumps({"yes": "注册成功"}), content_type="application/json")

def updatepassword(request):
    us = request.GET.get('username')
    old=request.GET.get('oldpassword')
    new =request.GET.get('newpassword')
    use=User.objects.get(username=us)
    if use.check_password(old):
        use.set_password(new)
        use.groups.add()
        use.save()
        logprint.loge("修改密码", us, "普通:" + us+"-修改了密码", "updateuser")
        return HttpResponse(json.dumps({"yes": "修改成功"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"yes": "修改失败,旧密码错误"}), content_type="application/json")


def cabupdate(request):
    newname = request.POST.get('fbname')
    oldname = request.POST.get('oldname')
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
    if oldname == newname:
        fibre = Fibre.objects.filter(FibreName=newname)
        fibre.update(FibreName=newname, Acap=acap, Aposition=apos, Aport=aport, Bcap=bcap,
                     Bposition=bpos, Bport=bport, MainMan=man, BkMan=bk, StartData=date)
        return render(request, 'polls/ok.html')
    if oldname != newname:
        if Fibre.objects.filter(FibreName=newname).exists():
            return render(request, 'polls/error.html')
        else:
            fibre = Fibre.objects.filter(FibreName=oldname)
            fibre.update(Cable=cabname, FibreName=newname, Acap=acap, Aposition=apos, Aport=aport, Bcap=bcap,
                         Bposition=bpos, Bport=bport, MainMan=man, BkMan=bk, StartData=date)
            return render(request, 'polls/ok.html')


def Yesupdate(request):
    newname = request.POST.get('fbname')
    oldname = request.POST.get('oldname')
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
    state = request.POST.get('state')

    if oldname == newname:
        if state != None:
            fibre = Fibre.objects.filter(FibreName=oldname)
            fibre.update(FibreName=newname, Acap=acap, Aposition=apos, Aport=aport, Bcap=bcap,
                         Bposition=bpos, Bport=bport, MainMan=man, BkMan=bk, StartData=date, STATE=state)
            logprint.loge("光纤修改", request.user.username, "修改"+newname, "update")
            return render(request, 'polls/ok.html')
        else:
            fibre = Fibre.objects.filter(FibreName=oldname)
            fibre.update(FibreName=newname, Acap=acap, Aposition=apos, Aport=aport, Bcap=bcap,
                         Bposition=bpos, Bport=bport, MainMan=man, BkMan=bk, StartData=date)
            logprint.loge("光纤修改", request.user.username, "修改"+newname, "update")
            return render(request, 'polls/ok.html')


def upFirbe(request):
    myFile = request.FILES.get("file", None)
    if myFile != None:
        Filename = myFile.name
        if Filename.endswith('.xlsx') and "光纤" in Filename:
            time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H-%I-%S")
            Ftime = time + "-" + Filename

            with open(BASE_DIR + Ftime, 'wb+') as destination:
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
                print("成功")
            errorlis = Save(request, Ftime)
            number = len(errorlis)
            if number == 0:
                logprint.loge("导入光纤路由成功", request.user.username, "", "up")
                return render(request, "polls/ok.html")
            else:
                logprint.loge("导入光纤路由有错误", request.user.username, "", "up")
                return render(request, 'polls/okk.html', {"error": errorlis, "num": number})
        else:
            return render(request, 'polls/no.html')
    else:
        return render(request, 'polls/nono.html')


def upCab(request):
    myFile = request.FILES.get("file", None)
    if myFile != None:
        Filename = myFile.name
        if Filename.endswith('.xlsx') and "光缆" in Filename:
            time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H-%I-%S")
            Ftime = time + "-" + Filename
            with open(BASE_DIR + Ftime, 'wb+') as destination:
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
            errorlis = SaveCab(request, Ftime)
            number = len(errorlis)
            if number==0:
                logprint.loge("导入光缆成功", request.user.username, "", "up")
                return render(request,"polls/ok.html")
            else:
                logprint.loge("导入光缆有错误", request.user.username, "", "up")
                return render(request, 'polls/okk.html', {"error": errorlis, "num": number})

        else:
            return render(request, 'polls/no.html')
    else:
        return render(request, 'polls/nono.html')


def upChannel(request):
    myFile = request.FILES.get("file", None)
    if myFile != None:
        Filename = myFile.name

        if Filename.endswith('.xlsx') and "波道" in Filename:
            time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H-%I-%S")
            Ftime = time + "-" + Filename
            with open(BASE_DIR + Ftime, 'wb+') as destination:
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
            errorlis = SaveChannel(request, Ftime)
            number = len(errorlis)
            if number == 0:
                logprint.loge("导入波道成功", request.user.username, "", "up")
                return render(request, "polls/ok.html")
            else:
                logprint.loge("导入波道有错误", request.user.username, "", "up")
                return render(request, 'polls/okk.html', {"error": errorlis, "num": number})
        else:
            return render(request, 'polls/no.html')
    else:
        return render(request, 'polls/nono.html')


def upWsr(request):
    myFile = request.FILES.get("file", None)
    if myFile != None:
        Filename = myFile.name

        if Filename.endswith('.xlsx') and "波道路由" in Filename:
            time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H-%I-%S")
            Ftime = time + "-" + Filename
            with open(BASE_DIR + Ftime, 'wb+') as destination:
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
            errorlis = SaveWsr(request, Ftime)
            number = len(errorlis)
            if number == 0:
                logprint.loge("导入波道路由成功", request.user.username, "", "up")
                return render(request, "polls/ok.html")
            else:
                logprint.loge("导入波道路由有错误", request.user.username, "", "up")
                return render(request, 'polls/okk.html', {"error": errorlis, "num": number})
        else:
            return render(request, 'polls/no.html')
    else:
        return render(request, 'polls/nono.html')
