# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=24)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
 
        return self.firstname