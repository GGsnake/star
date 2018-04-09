from adc.models import log

def loge(name,uid,context,tpp):
    log(logname=name,userid=uid,content=context,type=tpp).save()
def showloge(name,uid,context,tpp):
    log(logname=name,userid=uid,content=context,type=tpp).save()
