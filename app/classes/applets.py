# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, '.')
from .component import component
from .component import webMethod

class applets(component):
	def __init__(self):
		pass 
	@webMethod()
	def listApplets(self,request):
		path=os.path.dirname(os.path.abspath(__file__))
		sys.path.insert(0, path)
		files=os.listdir(path)
		applets=[]
		for fn in files:
			if(fn[-3:]==".py"):
				file=fn[:-3]
				mod = __import__('classes.'+file, fromlist=[file])
				applet=getattr(mod,file)
				if hasattr(applet, "isApplet"):
					applets.append({'appName':applet.appName,'appImg':applet.appImg,'appTitle':applet.appTitle})
		return applets
    


