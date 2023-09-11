# -*- coding: utf-8 -*-
import sys
import os
import math
sys.path.insert(0, 'L7')
from classes.appletbase import appletbase
from classes.appletbase import applet
from classes.component import webMethod
sys.path.insert(0, 'HW')
from HW.L7.File import File
from HW.L7.BenfordConf import BenfordConf
import uuid

@applet('benford',"Benford's Law",'benford.png')
class benford(appletbase):
    def __init__(self):
        pass;
    

   
    @webMethod()
    def preview(self,request,fid,maxLines):
        ret=""
        if "UID" in request.session:
            fuuid=uuid.UUID(fid)
            uid=int(request.session["UID"])
            files=File.objects.filter(uid=uid,id=fuuid)
            if len(files)==1:
                filename="userfiles/{0}/{1}".format(uid,fid)
                
                with open(filename, 'r',encoding="utf-8") as file:
                    while line := file.readline():  
                        ret=ret+line.rstrip()+"\r\n"
                        maxLines-=1
                        if(maxLines==0):
                            break;
 
        return ret
     
    @webMethod()
    def loadConf(self,request,fid):
        ret={}
        if "UID" in request.session:
            fuuid=uuid.UUID(fid)
            uid=int(request.session["UID"])
            fileConf=BenfordConf.objects.filter(file__id=fuuid)
            if len(fileConf)==1 and fileConf[0].file.uid==uid:
                ret={'hasHeader':fileConf[0].hasHeader,
                     'delimiter':fileConf[0].delimiter,
                     'quote':fileConf[0].quote,
                     'columnIndex':fileConf[0].columnIndex} 
        return ret

    @webMethod()
    def saveSettingsOnServer(self,request,fid,hasHeader,delimiter,quote,columnIndex):
        ret=False
        if "UID" in request.session:
            fuuid=uuid.UUID(fid)
            uid=int(request.session["UID"])
            file=File.objects.filter(id=fuuid)
            if len(file)==1:
                if file[0].uid==uid:
                    #proceed
                    bconf=BenfordConf.objects.filter(file=file[0])
                    if len(bconf)==0:
                        BenfordConf(hasHeader=hasHeader,delimiter=delimiter,quote=quote,columnIndex=columnIndex,file=file[0]).save()
                    else:
                        bconf[0].hasHeader=hasHeader
                        bconf[0].delimiter=delimiter
                        bconf[0].quote=quote
                        bconf[0].columnIndex=columnIndex
                        bconf[0].save();
                    ret=True
                    
                else:
                    raise Exception("Permission Denied")
        return ret;                
    
    
            
			