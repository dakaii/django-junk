from .models import Lesson, User, UserDetail, School, SchoolOwner, Booking
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.utils import load_backend


from .serializers import LessonSerializer, UserSerializer, UserDetailSerializer, SchoolSerializer
from .serializers import SchoolOwnerSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.decorators import login_required
#from .serializers import SignUpSerializer
#from oauth2_provider.views.generic import ProtectedResourceView
#from social.backends.oauth import BaseOAuth1, BaseOAuth2
#from social.exceptions import AuthAlreadyAssociated


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

@login_required
class SchoolOwnerViewSet(viewsets.ModelViewSet):
    queryset = SchoolOwner.objects.all()
    serializer_class = SchoolOwnerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    

@login_required
class UserDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly) 

class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset =Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)





"""
class Login(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Protected with OAuth2!')

@login_required
class Logout(ProtectedResourceView):
    def put(self, request, *args, **kwargs):
        return HttpResponse('Protected with OAuth2!')
    



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
