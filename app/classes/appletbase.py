# -*- coding: utf-8 -*-
from .component import component

def applet(name,title,img):
	def setApplet(func):
		func.isApplet=True
		func.appName=name
		func.appImg=img
		func.appTitle=title
		return func
	return setApplet

class appletbase(component):
	def __init__(self):
		pass;

