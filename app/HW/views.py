from django.shortcuts import render,HttpResponse
from django.http import FileResponse

from wsgiref.util import FileWrapper
import mimetypes
import re
import json 
import inspect
import logging
import uuid
import os
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from HW.L7.File import File
from HW.L7.BenfordConf import BenfordConf
logger = logging.getLogger('django')
import os

import io
import pandas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
#
def uploadFile(request):
    """
    Store the file an add a record to the db

    Parameters
    ----------
    request : HttpRequest 
        Django HttpRequest .

    Returns
    -------
    HttpResponse
        returns a stringfied json object 

    """
    uid=int(request.session["UID"])
    path="userfiles/{0}/".format(uid)
    ret=None
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            
        for filename, fileData in request.FILES.items():
            filename = request.FILES[filename].name
            file=File(uid=uid,filename=filename);
            with open(path+str(file.id), "wb+") as destination:
                for chunk in fileData.chunks():
                    destination.write(chunk)
                
            file.save()
        ret={'success':True,'msg':'','result':''}
    except Exception as e:
        ret={'success':False,'msg':str(e),'result':''}
    return HttpResponse(json.dumps(ret))
@csrf_protect
@ensure_csrf_cookie
def loadFile(request,fileName='index.html'):
    """
    

    Parameters
    ----------
    request : HttpRequest 
        Django HttpRequest .
    fileName : String, optional
        DESCRIPTION. The default is 'index.html'.
        the request file

    Returns
    -------
    FileResponse
        The requested file.

    """
    if fileName=='index.html':
        return HttpResponse(render(request,r'index.html',content_type="application/xhtml+xml"))
    else:
        fileName='files/'+fileName
        response =  FileResponse(FileWrapper(open(fileName, 'rb')), content_type=mimetypes.guess_type(fileName)[0])		
        return  response

def getTagContent(txt,tag):
    """
    Get the content of a html tag inside a text

    Parameters
    ----------
    txt : string
        input text.
    tag : string
        html tag.

    Returns
    -------
    string
        content of the tag.

    """
    return re.findall("(?<=\<"+tag+">)(.*?|[\s\S]+)(?=\</"+tag+">)",txt)[0]

def loadComponent(componentName):
    """
    Loads Vue's component

    Parameters
    ----------
    componentName : string
        DESCRIPTION.

    Returns
    -------
    None.

    """
    file = open(r"files/js/components/"+componentName+'.vue',mode='r')
    vueFile = file.read()
    file.close()
    script = getTagContent(vueFile,"script")
    lindex=script.index("{")
    rindex=script.rindex("}")
    
    script=script[lindex+1:rindex]
    template = json.dumps(getTagContent(vueFile,"template"))
    webMethods="{{{0}}}".format(",".join(getJavaScriptFunctions(componentName)))
    component='''const component = {{ template:{0}, {1} }};
if(component.methods){{
    component.methods=Object.assign({{}},component.methods,{2})
}}else{{
component.methods={2}
}}
export default component;'''.format(template,script,webMethods)
    ret = component
    return ret

def getWebMethods(className):
    webMethods=[]
    try:
        mod = __import__('classes.'+className, fromlist=[className])
        comClass = getattr(mod, className)

        for attrName in dir(comClass):
            attr=getattr(comClass, attrName)
            
            if hasattr(attr, "isWebMethod"):
                webMethods.append((attrName,attr))
    except Exception as e:
        
        logger.info(str(e))

    return webMethods

    
def getJavaScriptFunctions(className):
    webMethods=getWebMethods(className)
    jsFuncs=[]
    for funcInfo in webMethods:
        funcArgs=",".join(inspect.getfullargspec(funcInfo[1]).args[1:])
        jsFunc="{0}({1}){{let res=window.L7.callWebMethod('{2}','{0}',{1},false); return res;}}".format(funcInfo[0],funcArgs,className)
        jsFuncs.append(jsFunc)
        funcArgs+=",callBack"
        jsFunc="{0}Async({1}){{window.L7.callWebMethod('{2}','{0}',{1},true)}}".format(funcInfo[0],funcArgs,className)
        jsFuncs.append(jsFunc)
    return jsFuncs


def vueLoader(request, componentName):
    """
    

    Parameters
    ----------
    request : HttpRequest 
        Django HttpRequest .
    componentName : string
        name of the component.

    Returns
    -------
    HttpResponse
        Javascript code to load the component with template added as variable and webmethods attached to it.

    """
    return HttpResponse(loadComponent(componentName),content_type='text/javascript')
	
	
def webmethod(request,component,func):
	res=""
	success=True
	msg=""
	if request.method == "POST":
		paramsJSON=request.POST["params"]
		params=json.loads(paramsJSON)
		
		try:
			mod = __import__('classes.'+component, fromlist=[component])
			
			comClass = getattr(mod, component)
			
			obj=comClass()
			
			func=getattr(obj,func)
			params.insert(0,request)
	
			res=func(*params)
		except Exception as e:
			success=False
			msg=str(e)+"<br>"+paramsJSON
	ret={'success':success,'msg':msg,'result':res}
	return HttpResponse(json.dumps(ret))


def processBenford(path,delimiter,quote,header,columnIndex):
    ret=np.zeros(9)
    matplotlib.use('agg')
    try:
        df=pandas.read_csv(path,delimiter=delimiter,quotechar=quote,header=header,encoding = "ISO-8859-1")
        data=df[df.columns[columnIndex]]
        

        for i in range(len(data)):
            d=data[i]
            if not np.isnan(d):
                ind=int((d/(10**(np.floor(np.log10(d))))))
                ret[ind-1]+=1
        ret=100*ret/len(data)
    except Exception:
        pass
    
    x=np.arange(1,10)
    
    
    plt.clf()
    plt.xlabel('Digit',fontsize=15)
    plt.ylabel('%',fontsize=15)
    plt.rc('axes', titlesize=22)
    plt.rc('xtick', labelsize=15) 
    plt.rc('ytick', labelsize=15)
    plt.title("Benford's Law",fontsize=22)
    
    
    plt.plot(x,ret,'b',linewidth=5,label='Data')
    plt.plot(x,100*np.log10(1+1/x),'g*',markersize=15,label='Theory')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()

def benfordPlot(request,fid):
    if "UID" in request.session:
        fuuid=uuid.UUID(fid)
        uid=int(request.session["UID"])
        file=File.objects.filter(id=fuuid)
        if len(file)==1 and file[0].uid==uid:
            fileConf=BenfordConf.objects.filter(file=file[0])
            delimiter=","
            quote='"'
            columnIndex=0
            hasHeader=True
            if len(fileConf)==1:
                delimiter=fileConf[0].delimiter
                quote=fileConf[0].quote
                columnIndex=fileConf[0].columnIndex
                hasHeader=fileConf[0].hasHeader
            header=0 if hasHeader else None
            data=processBenford("userfiles/{0}/{1}".format(uid,fid),delimiter, quote, header, columnIndex)
            return HttpResponse(data, content_type="image/png")
                    
        else:
            return HttpResponse('Permission denied')