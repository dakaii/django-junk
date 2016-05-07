from geopy.geocoders import Nominatim
import json
from django.http import JsonResponse
from lessons.models import User, Password, Location
import pdb



def save_location(username,location):
	if not Location.objects.filter(location_name=location.raw['display_name'],longitude=location.longitude,latitude=location.latitude):
		location=Location.objects.create_location(location_name=location.raw['display_name'], longitude=location.longitude, latitude=location.latitude, address=location.address, registered_by=username, updated_by=username,boundingbox=location.raw['boundingbox'])
		return location
	return None


def get_location(request):
	location_name=request.POST.get('location_name')
	longitude=request.POST.get('longitude')
	latitude=request.POST.get('longitude')
	#pdb.set_trace()
	#print(request.user.is_authenticated())
	geolocator = Nominatim()
	if location_name is not None:
		location = geolocator.geocode(location_name)
	elif longitude is not None and latitude is not None:
		location = geolocator.reverse(latitude, longitude)
	return location

def user_location(location_name=None,username=None):
	geolocator = Nominatim()
	location = geolocator.geocode(location_name)
	try:
		location=Location.objects.get(location_name=location.raw['display_name'],longitude=location.longitude,latitude=location.latitude)
	except Location.DoesNotExist:
		location=save_location(username,location)
	except Location.MultipleObjectsReturned:
		location=Location.objects.filter(location_name=location_name,longitude=location.longitude,latitude=location.latitude).order_by('id').first()
		#I need to delete the rest.
	return location
