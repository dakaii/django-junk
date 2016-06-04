from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import json
from django.http import JsonResponse
from lessons.models import User, Password, Location
import pdb



def save_location(username,location):
	#pdb.set_trace()
	if not Location.objects.filter(location_name=location.raw['formatted_address'],longitude=location.longitude,latitude=location.latitude):
		location=Location.objects.create_location(location_name=location.raw['formatted_address'], longitude=location.longitude, latitude=location.latitude, address=location.address, registered_by=username, updated_by=username)
		return ({'result':True,'location':location})
	else:
		location=Location.objects.filter(location_name=location.raw['formatted_address'],longitude=location.longitude,latitude=location.latitude).order_by('id').first()
		return ({'result':False,'location':location})


def obtain_location_info(request):
	location_name=request.POST.get('location')
	longitude=request.POST.get('longitude')
	latitude=request.POST.get('longitude')
	#pdb.set_trace()
	#print(request.user.is_authenticated())
	geolocator=GoogleV3(api_key='AIzaSyBsm-cUdvx4PBcC0RjpZ7qEGxkhY-x9T18')
	#geolocator = Nominatim()
	if location_name is not None:
		location = geolocator.geocode(location_name,timeout=10)
	elif longitude is not None and latitude is not None:
		location = geolocator.reverse(latitude, longitude,timeout=10)
	return location



def user_location(location_name=None,username=None):
	geolocator = Nominatim()
	location = geolocator.geocode(location_name)
	try:
		location=Location.objects.get(location_name=location.raw['formatted_address'],longitude=location.longitude,latitude=location.latitude)
	except Location.DoesNotExist:
		location=save_location(username,location)['location']
	except Location.MultipleObjectsReturned:
		location=Location.objects.filter(location_name=location_name,longitude=location.longitude,latitude=location.latitude).order_by('id').first()
		#I need to delete the rest.
	return location
