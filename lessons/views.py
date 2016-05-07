from .models import Location, User, UserDetail, Tutor, Plan, Tag, Shop, Event
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import LocationSerializer, UserSerializer, UserDetailSerializer, ShopSerializer
from .serializers import EventSerializer, TagSerializer, PlanSerializer, TutorSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny#, IsAdminOrIsSelf
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .location import get_location, save_location

import pdb

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    def create(self, request, **kwargs):
        location=get_location(request)
        if location:
            if save_location(request.user.username,location) is not None:
                return Response({'successfully saved': location.raw['display_name']})
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
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    

#class PlanViewSet(viewsets.ReadOnlyModelViewSet):
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    #def create(self, request, **kwargs):


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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


