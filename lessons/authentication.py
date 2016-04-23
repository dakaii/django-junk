import logging
import requests
import json
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from random import randint
from django.conf import settings
from django.contrib.sessions.models import Session

from rest_framework import status

from lessons.models import User, Password
from lessons.serializers import SignUpSerializer, PasswordSerializer
from rest_framework import generics, renderers, viewsets

from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from lessons.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import detail_route, list_route

#from social.apps.django_app.utils import load_strategy, load_backend
#from social.backends.oauth import BaseOAuth1, BaseOAuth2
#from social.exceptions import AuthAlreadyAssociated
#from lessons.serializers import SocialSignUpSerializer


import pdb

class Login(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request):
		if request.POST.get('access_token') is not None:
			#pdb.set_trace()
			access_token = request.POST.get('access_token')
			graph_query = "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday&access_token={0}".format(access_token)
			try:
				user_data = requests.get(graph_query)
				user_jsonData=user_data.json()
				facebook_id=user_jsonData['id']
				try:
					user=User.objects.get(facebook_id=facebook_id)

				except User.DoesNotExist:
					username=user_jsonData['name'].replace (" ", "_")
					new_password=randint(1000000,9999999)
					password_store = Password.objects.create_password(password=new_password,facebook_id=facebook_id)
					user = User.objects.create_user(username=username,facebook_id=facebook_id,password=new_password)
				password = Password.objects.get(facebook_id=facebook_id)
				password=model_to_dict(password)
				user=model_to_dict(user)
				user = authenticate(username=user['username'], password=password['password'])
				if user is not None:
					if user.is_active:
						login(request,user)
						return Response("Successfully logged in.")
					else:
						return Response({"errors": "Error with social authentication1"},
								status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({"errors": "Error with social authentication2"},
								status=status.HTTP_400_BAD_REQUEST)
			except ConnectionError as e:    # This is the correct syntax
				return Response({"errors": "Error with social authentication3"},
							status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"errors": "Error with social authentication4"},
							status=status.HTTP_400_BAD_REQUEST)



class Logout(generics.CreateAPIView):
	permission_classes = (AllowAny,)

	#@login_required
	def create(self,request):
		#pdb.set_trace()
		logout(request)
		return Response("Successfully logged out.")






"""
class SocialSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SocialSignUpSerializer
    # This permission is nothing special, see part 2 of this series to see its entirety
    permission_classes = (IsAuthenticatedOrCreate,)

    def create(self, request, *args, **kwargs):

        pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = request.data['provider']

        # If this request was made with an authenticated user, try to associate this social 
        # account with it
        authed_user = request.user if not request.user.is_anonymous() else None

        # `strategy` is a python-social-auth concept referencing the Python framework to
        # be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA 
        # knows to use the Django strategy
        strategy = load_strategy(request)
        # Now we get the backend that corresponds to our user's social auth provider
        # e.g., Facebook, Twitter, etc.
        backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        if isinstance(backend, BaseOAuth1):
            # Twitter, for example, uses OAuth1 and requires that you also pass
            # an `oauth_token_secret` with your authentication request
            token = {
                'oauth_token': request.data['access_token'],
                'oauth_token_secret': request.data['access_token_secret'],
            }
        elif isinstance(backend, BaseOAuth2):
            # We're using oauth's implicit grant type (usually used for web and mobile 
            # applications), so all we have to pass here is an access_token
            token = request.data['access_token']

        try:
            # if `authed_user` is None, python-social-auth will make a new user,
            # else this social account will be associated with the user you pass in
            user = backend.do_auth(token, user=authed_user)
        except AuthAlreadyAssociated:
            # You can't associate a social account with more than user
            return Response({"errors": "That social media account is already in use"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            # if the access token was set to an empty string, then save the access token 
            # from the request
            auth_created = user.social_auth.get(provider=provider)
            if not auth_created.extra_data['access_token']:
                # Facebook for example will return the access_token in its response to you. 
                # This access_token is then saved for your future use. However, others 
                # e.g., Instagram do not respond with the access_token that you just 
                # provided. We save it here so it can be used to make subsequent calls.
                auth_created.extra_data['access_token'] = token
                auth_created.save()

            # Set instance since we are not calling `serializer.save()`
            serializer.instance = user
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, 
                            headers=headers)
        else:
            return Response({"errors": "Error with social authentication"},
                            status=status.HTTP_400_BAD_REQUEST)
 """




