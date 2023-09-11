# -*- coding: utf-8 -*-

from django.db import models
import uuid

class File(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	uid= models.IntegerField(default =0)
	filename= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True) 

	def __str__(self):
 
		return self.firstname