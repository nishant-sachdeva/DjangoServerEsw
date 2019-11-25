#! /usr/bin/env python3.7
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

import csv
from django.utils.encoding import smart_str
# here we will make our views from  the given data
# I am guessing we will be receiving data using the admin thing
# then we import it here, and the redirect it to our views I guess
from .models import Reading, Time, Identity

import json

import datetime
import pytz

# the functions get defined  here

# import sys
# sys.path.append('/home/usename/.local/lib/python3.7/site-packages/')

import requests
# import time


import urllib.request

TOKEN = "1022794746:AAHt1VVurUQZdpNb8MFeQVVmeceKGyk_soQ"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



def get_url(url):
    response = urllib.request.urlopen(url)
    print(response)
    # content = response.content.decode("utf8")
    # return content
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def call_bot(status):
    send_message(status, 746780062)
    send_message(status, 932176409)
    send_message(status, 659265902)


def download_data(request):
	# response content type
	response = HttpResponse(content_type='text/csv')
	#decide the file name
	response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.csv"'

	writer = csv.writer(response, csv.excel)
	response.write(u'\ufeff'.encode('utf8'))

	#write the headers
	writer.writerow([
		smart_str(u"Values"),
	])
	#get data from database or from text file....
	events = Reading.objects.all()[370:]
	for event in events:
		writer.writerow([
			smart_str(event.value),
		])
	return response


def send_post_to_onem2m(status , value):
    print(1)
    # cse_ip = "onem2m.iiit.ac.in"
    # server = "https://" + cse_ip + "/~/in-cse/in-name/"
    # ae = "Team35_Street_lighting_And_building_entrances_based_on_daylight"
    # cnt = "node_1"

    # url = server + ae + "/" + cnt + "/"
    # payload = {
    #     "m2m:cin": {
    #         "cnf": "text/plain:0",
    #         "con": "test"
    #     }
    # }
    # headers = {
    #     "X-M2M-Origin": "admin:admin",
    #     "Content-Type": "application/json;ty=4",
    #     "Content-Length": "100",
    #     "Connection": "close"
    # }

    # r = requests.post(url, data=json.dumps(payload), headers=headers)
    # call_bot(url)
    # call_bot("Return value from onem2m server is "  + str(r))

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

		current_time = pytz.utc.localize(datetime.datetime.utcnow())
		now = current_time.astimezone(pytz.timezone("Asia/Kolkata"))

		reading_obj = Reading(value = y , status = x, time = now)
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

		# around here , we will send the post requests to the servers at onem2m
		try:
		    send_post_to_onem2m(y , x)  # y is the value and x is the status
		except Exception as e:
		    call_bot(str(e) +  "is the error")
		    print("onem2m failed")

		if reading_obj.status == 1 :
			call_bot("Lights are ON. Current reading is " +  str(y))
		else:
			call_bot("Lights are OFF. Current reading is  " + str(y))
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

	l = []
	s = Reading.objects.values()
	s = s[(s.count()-50):]
	for a in s:
		l.append(a['value'])

	rate = 6.6

	our_cost = rate * time_obj.total_time
	normal_cost = rate * (int(time_obj.total_time/12))*13



	context = {
		"list" : {
			"id":id_to_be_showed,
			"value" :val,
			"status" : stat,
			"time" : obj.time,
			"total_time" : round(time_obj.total_time , 2),
			"redirect_url" : "https://localhost:8000/",
			"set_of_values" : l,
			"our_cost" : our_cost,
			"normal_cost" : normal_cost,
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


