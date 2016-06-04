from .models import Location, User, Tutor, Schedule, Tag, Shop, Event
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import LocationSerializer, UserSerializer,UserDetailSerializer, ShopSerializer
from .serializers import EventSerializer, TagSerializer, ScheduleSerializer, TutorSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny#, IsAdminOrIsSelf
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .location import obtain_location_info, save_location

import pdb

class LocationViewSet(viewsets.ModelViewSet):
	queryset = Location.objects.all()
	serializer_class = LocationSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	def create(self, request, **kwargs):
		location=obtain_location_info(request)
		if location:
			if save_location(request.user.username,location)['result']:
				return Response({'successfully saved': location.raw['formatted_address']})
			else:
				return Response({"errors": "This data already exists in the database."},
									status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"errors": "probably not enough argumnets provided"},
									status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class UserDetailViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)  

class ScheduleViewSet(viewsets.ModelViewSet):
	queryset = Schedule.objects.all()
	serializer_class = ScheduleSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ShopViewSet(viewsets.ModelViewSet):
	queryset = Shop.objects.all()
	serializer_class = ShopSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	def create(self, request, **kwargs):
		shop_name=request.POST.get('shop_name')
		shop_owner=request.user
		try:
			location=obtain_location_info(request)
			location=save_location(request.user.username,location)['location']
		except Exception:
			return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)
		try:
			shop=Shop.objects.get(shop_name=shop_name,shop_location=location)
			return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)
		except Shop.DoesNotExist:
			shop = Shop.objects.create_shop(shop_name=shop_name, user_editable=True, registered_by=shop_owner, updated_by=shop_owner, shop_owner=shop_owner, shop_location=location)
			return Response({'successfully saved': shop.shop_name})
		except Shop.MultipleObjectsReturned:
			shop=Shop.objects.filter(shop_name=shop_name,location=location).order_by('id').first()
			return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	def create(self, request, **kwargs):
		title=request.POST.get('title')
		username=request.user.username
		start_time = request.POST.get('start_time')
		end_time = request.POST.get('end_time')
		time_type = request.POST.get('time_type')
		try:
			location=obtain_location_info(request)
			location=save_location(request.user.username,location)['location']
			if request.POST.get('shop_name') is not None:
				shop=Shop.objects.filter(shop_name=request.POST.get('shop_name'),shop_location=location).order_by('id').first()
				location=shop.shop_location
			else:
				shop=None
		except Exception:
			return Response({"errors": "The provided info could not be validated."},status=status.HTTP_400_BAD_REQUEST)
		try:
			event=Event.objects.get(title=title,location=location)
			return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)
		except Event.DoesNotExist:
			event = Event.objects.create_event(title=title, date=request.POST.get('date'), day_of_week=request.POST.get('day_of_week'), start_time=start_time, end_time=end_time, time_type=time_type, registered_by=username, updated_by=username, shop=shop, location=location)
			return Response({'successfully saved': event.title})
		except Event.MultipleObjectsReturned:
			shop=Shop.objects.filter(title=title,location=location).order_by('id').first()
			return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class TutorViewSet(viewsets.ModelViewSet):
	queryset = Tutor.objects.all()
	serializer_class = TutorSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



class CustomObtainAuthToken(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
		token = Token.objects.get(key=response.data['token'])
		return Response({'token': token.key, 'id': token.user_id})


