# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '.')
from .component import component
from .component import webMethod
import sys
sys.path.insert(0, 'HW')
from HW.L7.User import User


class loginMenu(component):
    def __init__(self):
        pass
	
	
    @webMethod()
    def isLogined(self,request):
        ret=None
        
        if "UID" in request.session:
            user=User.objects.filter(id=int(request.session['UID']))
            if len(user)==1:
                ret={'firstname':user[0].firstname,'lastname':user[0].lastname}
        return ret
    
    @webMethod()
    def logout(self,request):
        ret=False
        if "UID" in request.session:
            request.session.pop("UID")
            ret=True
        return ret;