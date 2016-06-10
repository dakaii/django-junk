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
from lessons.serializers import SignUpSerializer
from rest_framework import generics, renderers, viewsets

from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from lessons.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token
from .location import user_location, obtain_location


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
                user_json = requests.get(graph_query).json()
                username = user_json['name']
                facebook_id = user_json['id']
                email = user_json['email']
                location_name = user_json['location']['name']; longitude = None; latitude = None;
                new_password = None
                if not Password.objects.filter(email=email):
                    new_password = User.objects.make_random_password()
            except ConnectionError:
                return Response({"errors": "connection error"},
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.POST.get('email') is not None and request.POST.get('password') is not None\
                and request.POST.get('username') is not None and request.POST.get('location') is not None:
            username = request.POST.get('username')
            facebook_id = None
            email = request.POST.get('email')
            location_name = request.POST.get('location'); longitude = request.POST.get('longitude'); latitude = request.POST.get('latitude')
            new_password = request.POST.get('password')
        else:
            return Response({"errors": "Not enough arguments"},
                            status=status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------
        if User.objects.filter(email=email) is None and User.objects.filter(username=username) is None:
            location = obtain_location(request, location_name, longitude, latitude)
            if location is not None:
                location = user_location(location=location, username=username)
                password = Password.objects.create_password(password=new_password, email=email)
                # authentication fails when there's already a password in the password table but the user doesnt exist.
                user = User.objects.create_user(username=username,facebook_id=facebook_id,password=password.password,email=email,location=location)
            else:
                return Response({"error": "unable to obtain the location info."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(email=email, username=username).order_by('id').first()
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user_id=user.id)

            if user.is_active:
                return JsonResponse({'id':user.id,'token':token.key,})
            else:
                return Response({"error": "Error. User is no longer active."},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "The provided info could not be validated."},
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


