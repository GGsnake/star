
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render

from adc import logprint


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if password and username:
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            ip = request.META.get("REMOTE_ADDR", None)
            logprint.loge("登录", username, "IP:"+ip, "login")
            return HttpResponseRedirect("index")
        else:
            return render(request, 'polls/loginerror.html')
    else:
         return render(request, 'polls/loginerror.html')
def logis(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if password and username:
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            ip = request.META.get("REMOTE_ADDR", None)
            logprint.loge("登录", username, "IP:"+ip, "login")
            return HttpResponseRedirect("index")
        else:
            return render(request, 'polls/loginerror.html')
    else:
         return render(request, 'polls/loginerror.html')

def loginindex(request):
    return render(request, 'polls/newlogin.html')

def loginout(request):
    logprint.loge("退出登录", request.user.username, "用户:"+request.user.username, "loginout")
    auth.logout(request)
    return HttpResponseRedirect("login")
