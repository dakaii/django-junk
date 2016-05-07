import requests
import json
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from random import randint
from django.conf import settings
from django.http import JsonResponse

from rest_framework import status

from lessons.models import User, Password, Location
from lessons.serializers import SignUpSerializer, PasswordSerializer
from rest_framework import generics, renderers, viewsets
from geopy.geocoders import Nominatim

from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from lessons.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token
from .location import user_location


import pdb


class Login(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request):
		if request.POST.get('access_token') is not None:
			access_token = request.POST.get('access_token')
			graph_query = "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday%2Cemail&access_token={0}".format(access_token)
			try:
				user_data = requests.get(graph_query)
				user_jsonData=user_data.json()
				username=user_jsonData['name']
				facebook_id=user_jsonData['id']
				email = user_jsonData['email']
				location_name=user_jsonData['location']['name']
				if not Password.objects.filter(email=email):
					new_password = User.objects.make_random_password()
			except ConnectionError as e:
				return Response({"errors": "Error with social authentication3"},
							status=status.HTTP_400_BAD_REQUEST)

		elif request.POST.get('email') is not None and request.POST.get('password') is not None:
			if request.POST.get('username') is not None and request.POST.get('location') is not None:
				email=request.POST.get('email')
				new_password=request.POST.get('password')
				username=request.POST.get('username')
				location_name=request.POST.get('location')
				facebook_id=None

			try:
				user=User.objects.get(email=email)
			except User.DoesNotExist:
				location = user_location(location_name=location_name,username=username)
				password=Password.objects.create_password(password=new_password,email=email)
				# authentication fails when theres already a password in the password table but the user doesnt exist.
				user = User.objects.create_user(username=username,facebook_id=facebook_id,password=password.password,email=email,location=location)
			try:
				token = Token.objects.get(user_id=user.id)
			except Token.DoesNotExist:
				token = Token.objects.create(user_id=user.id)

			if user.is_active:
				return JsonResponse({'id':user.id,'token':token.key,})
			else:
				return Response({"errors": "Error. User is no longer active."},
						status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"errors": "Error with social authentication4"},
							status=status.HTTP_400_BAD_REQUEST)



class Logout(generics.DestroyAPIView):
	queryset = Token.objects.all()
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

	def delete(self, request):
		try:
			token = Token.objects.get(user_id=request.user.id)
			token.delete()
		except Token.DoesNotExist:
			return Response('already logged out', status=status.HTTP_404_NOT_FOUND)
		return Response(status=status.HTTP_204_NO_CONTENT)


