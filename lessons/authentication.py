import requests
import json
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict


from rest_framework import status
from .models import User
from .serializers import SignUpSerializer
from rest_framework import generics, renderers, viewsets
from oauth2_provider.views.generic import ProtectedResourceView
#from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.exceptions import AuthAlreadyAssociated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route, list_route





"""
#idk how yet, but the url below gets sent here.
url = "https://heroku?access_token=CAAJGUqTLHZAkBAE4wsNRnrtUQOhcFZCtAiofAOGVWsrMIaMGEUXTg2nm9Dqq4uGoDjp3le4YWKppNeotWj8r3Ju3MRJPN7arhdLUmXp8CueJzZAHTjFMCCsrYfTqy6OyrGfDUMYxgCEUw0ZCcjnivTyzBNhlQ0jqlbtUkurZAKrIt6O2DGKEu2sEKtL8YKBZBd3PB479eZAKAZDZD"
parse_result=urlparse(url)
query = parse_qs(parse_result.query)
access_token = query['access_token'][0]
print(access_token)

access_token='EAAJGUqTLHZAkBADnruUh3dcVJenZAEQQotEbZBW6BEfLzWPi6bKm0P4YXdbBvBCkTJpjk2W82IJBhLXZB2CVF0Tx24UDjKgbQxhRLIStGwlHNLco1Uj6aclsPTZBtdRbrOQTYjHo0eYR86Mr1RxvDUCTiYgO37h6TK2knj0gxFgZDZD'
graph_query = "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday&access_token={0}".format(access_token)

user_data = requests.get(graph_query)

"""




class Login(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request):
		if request.GET.get('access_token'):
			access_token = request.GET.get('access_token')
			graph_query = "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday&access_token={0}".format(access_token)
			try:
				user_data = requests.get(graph_query)
				user_jsonData=user_data.json()
				try:
					user=User.objects.get(id=user_jsonData['id'])

				except User.DoesNotExist:
					user =User(username=user_jsonData['name'],id=int(user_jsonData['id']))
					user.save()
					#I might need to make two separate cases for tutors and tutees.
					#I need to generate a random and unique password for each user.
			user=model_to_dict(user)
			user = authenticate(username=user['username'], password=user['password'])
			#login(request, user)
			except ConnectionError as e:    # This is the correct syntax
				return Response({"errors": "Error with social authentication"},
							status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"errors": "Error with social authentication"},
							status=status.HTTP_400_BAD_REQUEST)





#@detail_route(methods=['post'])
#@login_required
class Logout(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer	
	@login_required
	def destroy(self, request, pk=None):
		return HttpResponse('Protected with OAuth2!')
	


"""
class SocialSignUp(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	# This permission is nothing special, see part 2 of this series to see its entirety
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request, *args, **kwargs):

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
