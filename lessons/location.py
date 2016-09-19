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
