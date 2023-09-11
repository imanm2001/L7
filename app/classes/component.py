# -*- coding: utf-8 -*-
def webMethod():
	def setWebMethod(func):
		func.isWebMethod=True
		return func
	return setWebMethod
class component:
	def __init__(self):
		pass;