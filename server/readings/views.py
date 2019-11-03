from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

# here we will make our views from  the given data
# I am guessing we will be receiving data using the admin thing
# then we import it here, and the redirect it to our views I guess
from .models import Reading, Time, Identity

import json

import datetime
import pytz 

# the functions get defined  here

def checkreq(request):
	'''
	so here's the deal, this guy takes in the request and works on it
	it loads the value and status from the json object that has been received
	makes a reading object based on that
	saves it

	no, if the status is 1, that means it has been  10 more minutes since the last reading, hence we add 1/6 ht of an hour to the total time

	now we update the identiity object to store the identity of the lastest object
	this identity will keep updating with every new object

	so at the end of the function . we have the new data in a new object , we have the latest id and we have the totol running time for upto now

	this all will be there in the data base for further use
	'''


	x = 0
	y = -1
	if request.method == "POST":
		print(request.body)
		x = json.loads(request.body)['status']
		y = json.loads(request.body)['value']


		reading_obj = Reading(value = y , status = x)
		reading_obj.save()	

		# now we update time 
		if x == 1:
			time_obj = Time.objects.get(id=1)
			time_obj.total_time += float(1/6)
			time_obj.save()

		# now we update the identit
		id_object = Identity.objects.get(id=1)
		id_object.Identity  = reading_obj.id
		id_object.save()
		# so now  we have the identity of the new object

		return HttpResponse(status=201)
	else:
		return HttpResponse("<h1>GET request intercepted successfully</h1>")


def home_view(request, *args, **kwargs):
	'''
	so here is the deal for this function, we have the latest id, in case that dosen't work, we will have the default base.html page to take care of our things, 

	latest id retrieved:
	latest object retrieved for the object
	total time retrieved

	make a context object for all these things

	display on the final web page

	'''
	print(request)
	print(Identity)
	
	id_object = Identity.objects.get(id=1)
	id_to_be_showed = id_object.Identity

	if id_to_be_showed == 1:
		return render(request, "base.html", {})

	obj = Reading.objects.get(id = id_to_be_showed)
	val = obj.value
	stat = obj.status

	time_obj = Time.objects.get(id=1)

	
	current_time = pytz.utc.localize(datetime.datetime.utcnow())
	now = current_time.astimezone(pytz.timezone("Asia/Kolkata"))
	# now = timezone.now() 

	context = {
		"list" : {
			"id":id_to_be_showed,
			"value" :val,
			"status" : stat,
			"time" : now ,
			"total_time" : round(time_obj.total_time , 2),
			"redirect_url" : "https://localhost:8000/"
		},
	}	
	return render(request, "home.html", context)

'''
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"value":1111,"status":"0"}' \
  http://127.0.0.1:8000/reading
  csrftoken:"af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS"

curl -d "status=1&value=100&csrfmiddlewaretoken=af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS" http://127.0.0.1:8000/reading/


curl http://127.0.0.1:8000/reading/ \
 -X POST \
 -H "Content-Type: application/json" \
 -H "Accept: text/html,application/json" \
 -H "X-CSRFToken: af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS" \
 -H "Cookie: csrftoken=af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS" \
 -d '{"value":12133 , "status":1}'

'''


