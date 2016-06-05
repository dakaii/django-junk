from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import json
from django.http import JsonResponse
from lessons.models import User, Password, Location
import pdb



def save_location(username,location_name, original_id, access, city, state, zipcode, longitude, latitude, address, county_code):
	if not Location.objects.filter(location_name=location_name,longitude=location.longitude,latitude=location.latitude):
		location=Location.objects.create_location(location_name=location_name, original_id=original_id, access=access, city=city, state=state, zipcode=zipcode, longitude=longitude, latitude=latitude, address=address, county_code=county_code, registered_by=username, updated_by=username)
		return ({'result':'success','location':location})
	else:
		location=Location.objects.filter(location_name=location.raw['formatted_address'],longitude=location.longitude,latitude=location.latitude).order_by('id').first()
		return ({'result':'duplicate','location':location})

def obtain_location(request):
	location_name=request.POST.get('location')
	longitude=request.POST.get('longitude')
	latitude=request.POST.get('longitude')
	geolocator=GoogleV3(api_key='AIzaSyBsm-cUdvx4PBcC0RjpZ7qEGxkhY-x9T18')
	if location_name is not None:
		location = geolocator.geocode(location_name,timeout=10)
	elif longitude is not None and latitude is not None:
		location = geolocator.reverse(latitude, longitude,timeout=10)
	return location


def user_location(location_name,username):
	geolocator=GoogleV3(api_key='AIzaSyBsm-cUdvx4PBcC0RjpZ7qEGxkhY-x9T18')
	location = geolocator.geocode(location_name)
	try:
		location=Location.objects.get(location_name=location.raw['formatted_address'],longitude=location.longitude,latitude=location.latitude)
	except Location.DoesNotExist:
		location=save_location(username,location_name=location.raw['formatted_address'], original_id=None, access=None, city=None, state=None, zipcode=None, longitude=location.raw['geometry']['location']['lng'], latitude=location.raw['geometry']['location']['lat'], address=location.raw['formatted_address'], county_code=None)['location']
	except Location.MultipleObjectsReturned:
		location=Location.objects.filter(location_name=location_name,longitude=location.longitude,latitude=location.latitude).order_by('id').first()
		#I need to delete the rest.
	return location
