import json
from django.shortcuts import render
from django.http import HttpResponse

from multiprocessing.managers import BaseManager


#['GetRecipe', 'GetState', 'Main', 'SetRecipe', 'Start', 'StartBoil', 'StartCock', 'Stop', 'StopBoil', 'StopCock', 'WaitForState', '_Client', '__builtins__', '__class__', '__deepcopy__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_address_to_local', '_after_fork', '_authkey', '_callmethod', '_close', '_connect', '_decref', '_exposed_', '_getvalue', '_id', '_idset', '_incref', '_isauto', '_manager', '_mutex', '_serializer', '_tls', '_token']
#temperatura, 2 uscite dig, desc stato, ricetta id


class RaspBeerManager(BaseManager): pass
RaspBeerManager.register('get_controller')
m = RaspBeerManager(address=('localhost', 12345), authkey='raspbeer')
m.connect()
client = m.get_controller()


#url(r'^controller/temp/$', name='get_temperature'),
def get_temperature(request):
	resp = {'status':0, 'temp':0}
	
	
	
	return HttpResponse(json.dumps(resp), content_type="application/json")
	

#url(r'^controller/info/$', name='get_info'),
def get_info(request):
	resp = {'status':0, 'temp':0}
	
	print dir(client)
	client.Start()
	print client.GetState()
	info_dict = client.GetInfo()
	
	return HttpResponse(json.dumps(info_dict), content_type="application/json")


#	url(r'^controller/start/$', name='start_raspbeer'),
def start_raspbeer(request):
	resp = {'status':0, 'stato':0}
# 	m = RaspBeerManager(address=('localhost', 12345), authkey='raspbeer')
# 	m.connect()
# 	client = m.get_controller()
	
	
	#print dir(client)
	client.Start()
	print client.GetState()
	
	#resp['stato'] = stato
	
	return HttpResponse(json.dumps(resp), content_type="application/json")
	
	
	