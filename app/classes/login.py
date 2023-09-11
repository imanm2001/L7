# -*- coding: utf-8 -*-

from .component import component
from .component import webMethod
import sys
sys.path.insert(0, 'HW')
from HW.L7.User import User

class login(component):
    def __init__(self):
        pass 

    @webMethod()
    def createAccount(self,request,firstname,lastname,username,password):
        username=username.lower()
        usrs=User.objects.filter(username=username)
        ret=False;
        if len(usrs)==0:
            usr=User(firstname=firstname,lastname=lastname,username=username,password=password)
            usr.save()
            ret=True
        return ret;
    @webMethod()
    def loginUser(self,request,username,password):
        ret=False
        username=username.lower()
        usrs=User.objects.filter(username=username,password=password).only('firstname','lastname')
        if len(usrs)==1:
            ret={'username':username,'firstname':usrs[0].firstname,'lastname':usrs[0].lastname}
            request.session["UID"]=usrs[0].id
        return ret