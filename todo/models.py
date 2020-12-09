from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import datetime
from django.utils import timezone

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	creationdate = models.DateTimeField('Date Created', default=timezone.now)
	backgroundimage = models.TextField(default='http://i.imgur.com/v7X0tLG.jpg')
	#backgroundimage = models.Imagefield() #For Future Use!

	def __unicode__(self):
		return self.user.username


class Task(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	text = models.TextField()
	creationdate = models.DateTimeField('Date Created', default=timezone.now) 
	duedate = models.DateTimeField('Date Due', default=timezone.now)

	def __unicode__(self):
		return self.text

