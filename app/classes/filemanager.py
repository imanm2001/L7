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
import uuid

@applet('filemanager','File Manager','filemanager.png')
class filemanager(appletbase):
    def __init__(self):
        pass;
    

    @webMethod()
    def delFile(self,request,fid):
        fuuid=uuid.UUID(fid)
        uid=int(request.session["UID"])
        files=File.objects.filter(id=fuuid,uid=uid)
        ret=False
        if len(files)==1:
            files.delete();
            path="userfiles/{0}/{1}".format(uid,fid)
            os.remove(path)
            ret=True
                
        
        return ret
    @webMethod()
    def listFiles(self,request,index):
        uid=int(request.session["UID"])
        files=File.objects.filter(uid=uid)
        totalPages=max(1,math.ceil(len(files)/10.0))
        fileData=[]
        start=(index-1)*10;
        for i in range(start,min(start+10,len(files))):
            file=files[+i]
            fileData.append({'id':str(file.id),'filename':file.filename,'date':file.created_at.strftime("%m/%d/%Y, %H:%M:%S")})
        ret={'totalPages':totalPages,'files':fileData}
        return ret;
		
			