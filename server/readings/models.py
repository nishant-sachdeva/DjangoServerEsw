from django.db import models

# Create your models here.

# create design of the model here , 
class Reading(models.Model):
	value = models.IntegerField(default = 0)
	status = models.IntegerField(default = 0)
	# this defines our thing very easily
	# we have the reading of the sunlight
	# the status will tell us if the light has been on/off
	def __str__(self):
		# print(str(self.id) +" "+ str(self.value) + " " + str(self.status))
		ret = str(self.id) +" "+ str(self.value) + " " + str(self.status)
		return ret

