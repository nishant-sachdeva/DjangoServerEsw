from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

# here we will make our views from  the given data
# I am guessing we will be receiving data using the admin thing
# then we import it here, and the redirect it to our views I guess
from .models import Reading, Time

import json

# the functions get defined  here

now = timezone.now()

def checkreq(request):
	x = 0
	y = -1
	if request.method == "POST":
		print(request.body)
		x = json.loads(request.body)['status']
		y = json.loads(request.body)['value']

		now = timezone.now()
		
		obj = Reading(value = y , status = x)

		obj.save()	

		# now we update time 
		if x == 1:
			obj = Time.objects.get(id=1)
			obj.total_time += float(1/6)
			obj.save()

		# now we update the identit
		id_object = Identity.objects.get(id=1)
		id_object.Identity  = obj.id
		id_object.save()
		# so now  we have the identity of the new object

		context = {
			"list" : {
				"value" : y,
				"status" : x,
				"time" : timezone.now(),
				"text" : "ID just created is " + str(obj.id) , 
			},
		}
		print(Identity)
		return HttpResponse(status=201)
	else:
		return HttpResponse("<h1>GET request intercepted successfully</h1>")


def home_view(request, *args, **kwargs):
	# now = timezone.now()
	print(request)
	print(Identity)
	print(ab)
	
	id_object = Identity.objects.get(id=1)
	id_to_be_showed = id_object.Identity

	obj = Reading.objects.get(id = id_to_be_showed)

	val = obj.value
	stat = obj.status
	context = {
		"list" : {
			"id":id_to_be_showed,
			"value" :val,
			"status" : stat,
			"time" : now 
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


