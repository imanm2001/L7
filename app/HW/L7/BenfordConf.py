# -*- coding: utf-8 -*-

from django.db import models
import uuid
from .File import File

class BenfordConf(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE)
    delimiter= models.CharField(max_length=255,default='"')
    quote= models.CharField(max_length=255,default=',')
    hasHeader = models.BooleanField(default=False)
    columnIndex = models.IntegerField(default=0)
    
    def __str__(self):
        
        return self.firstname