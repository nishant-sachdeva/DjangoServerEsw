from django.db import models

# Create your models here.

# create design of the model here ,
class Reading(models.Model):
	value = models.IntegerField(default = 0)
	status = models.IntegerField(default = 0)
	time = models.DateTimeField(auto_now_add=True)

	# this defines our thing very easily
	# we have the reading of the sunlight
	# the status will tell us if the light has been on/off

	def __str__(self):
		# print(str(self.id) +" "+ str(self.value) + " " + str(self.status))
		ret = str(self.id) +" "+ str(self.value) + " " + str(self.status)
		return ret

class Time(models.Model):
	total_time = models.FloatField(default=0.0)


class Identity(models.Model):
	Identity = models.IntegerField(default=0)


class Mode(models.Model):
	mode = models.IntegerField(default=0)
	# 0 means manual, 1 means auto

class Status(models.Model):
	status = models.IntegerField(default=0)
	# o means OFF and 1 means On

