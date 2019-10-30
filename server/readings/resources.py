from tastypie.resources import ModelResource 
from readings.models import Reading
from tastypie.authorization import Authorization



class ReadingResource(ModelResource):
	class Meta:
		queryset = Reading.objects.all()
		resource_name = 'Reading'
		authorization = Authorization()
		fields = ['value' , 'status']
