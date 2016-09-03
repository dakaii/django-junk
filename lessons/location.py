from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import json
from django.http import JsonResponse
from lessons.models import User, Password, Location
from django.utils.translation import to_locale, get_language
import pdb


def save_location(username, location_name, original_id, access, city, state, zipcode, longitude, latitude, address, country_code):
    if not Location.objects.filter(location_name=location_name, longitude=longitude, latitude=latitude):
        location = Location.objects.create_location(location_name, original_id, access, city, state=state,
                                                    zipcode=zipcode, longitude=longitude, latitude=latitude,
                                                    address=address, country_code=country_code, registered_by=username,
                                                    updated_by=username)
        return {'result': 'success', 'location': location.location_name, 'longitude': location.longitude, 'latitude': location.latitude}
    else:
        location=Location.objects.filter(location_name=location_name, longitude=longitude, latitude=latitude).order_by('id').first()
        return {'result': 'duplicate', 'location': location.location_name, 'longitude': location.longitude, 'latitude': location.latitude}

"""
def obtain_location(request, location_name=None, longitude=None, latitude=None):
    geolocator = GoogleV3(api_key='AIzaSyBsm-cUdvx4PBcC0RjpZ7qEGxkhY-x9T18')
    if location_name is not None:
        location = geolocator.geocode(location_name, timeout=10, language=request.LANGUAGE_CODE)

    elif longitude is not None and latitude is not None:
        location = geolocator.reverse(latitude, longitude, timeout=10, language=request.LANGUAGE_CODE)
    else:
        location = None
    if location is not None:
        location_name = address = location.raw['formatted_address']
        longitude = location.raw['geometry']['location']['lng']
        latitude = location.raw['geometry']['location']['lat']
        original_id = location.raw['place_id']
        return {"location_name": location_name, "address": address, "longitude": longitude, "latitude": latitude,
                "original_id": original_id}
    else:
        return None


def user_location(location, username):
    #location_name, address = "_".join([x['long_name'] for x in location.raw['address_components']])
    location_name = location['location_name']; longitude = location['longitude']; latitude = location['latitude']
    original_id = location['original_id']; address = location['address']
    try:
        location = Location.objects.get(location_name=location_name, longitude=longitude, latitude=latitude)
    except Location.DoesNotExist:
        location = save_location(username=username, location_name=location_name, original_id=original_id, access=None, city=None,
                                 state=None, zipcode=None, longitude=longitude, latitude=latitude, address=address,
                                 country_code=None)['location']
    except Location.MultipleObjectsReturned:
        location=Location.objects.filter(location_name=location_name, longitude=longitude, latitude=latitude).order_by('id').first()
        #I need to delete the rest.
    return location
"""