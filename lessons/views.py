from .models import Location, User, Tutor, Schedule, Tag, Shop, ShopItem, Event, Course
#from .models import TagMapping, DataPictureMapping
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import LocationSerializer, UserSerializer,UserDetailSerializer, ShopSerializer, ShopItemSerializer
from .serializers import EventSerializer, TagSerializer, ScheduleSerializer, TutorSerializer, CourseSerializer
#from .serializers import TagMappingSerializer, DataPictureMappingSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny#, IsAdminOrIsSelf
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .location import save_location#, obtain_location
import pdb



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def create(self, request, **kwargs):
        try:
            location_name = request.POST.get('location_name'); original_id = request.POST.get('original_id')
            access = request.POST.get('access'); city=request.POST.get('city'); state=request.POST.get('state')
            zipcode = request.POST.get('zipcode');  longitude=request.POST.get('longitude'); latitude=request.POST.get('latitude')
            address = request.POST.get('address'); country_code = request.POST.get('country_code')
            result = save_location('chime', location_name, original_id, access, city, state, zipcode, longitude, latitude, address, country_code)['result']
            return Response(result)
            if save_result['result'] == 'success':
                return Response({'status': 'successfully saved'})
            elif save_result['result'] == 'duplicate':
                return Response({"status": "This data already exists in the database."},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": "Connection timeout"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
"""
    def create(self, request, **kwargs):
        if request.POST.get('datastore'):
            # nothing
        else:
            #
"""

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def create(self, request, **kwargs):
        shop_name=request.POST.get('shop_name')
        cuisine_type=request.POST.get('cuisine_type')
        referUrl=request.POST.get('referUrl')
        tel=request.POST.get('tel')
        shop_location=request.POST.get('shop_location')
        shop_owner=request.user
        shop_owner_name = request.user.username
        try:
            shop=Shop.objects.get(shop_name=shop_name,shop_location=shop_location)
            return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)
        except Shop.DoesNotExist:
            shop = Shop.objects.create_shop(shop_name=shop_name, cuisine_type=cuisine_type, referUrl=referUrl,tel=tel, registered_by=shop_owner_name, updated_by=shop_owner_name, shop_owner=shop_owner, shop_location=shop_location)
            return Response({'successfully saved': shop.shop_name})
        except Shop.MultipleObjectsReturned:
            shop=Shop.objects.filter(shop_name=shop_name,location=location).order_by('id').first()
            return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)


class ShopItemViewSet(viewsets.ModelViewSet):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def create(self, request, **kwargs):
        item_name=request.POST.get('item_name')
        image_url=request.POST.get('image_url')
        item_description=request.POST.get('item_description')
        price=request.POST.get('price')
        category=request.POST.get('category')
        shop_name=request.POST.get('shop_name')
        shop_location = request.POST.get('shop_location')
        #user_name = request.user.username
        try:
            shop=Shop.objects.get(shop_name=shop_name,shop_location=shop_location)
        except Exception:
            return Response({"errors": "the shop associated with the item was not found."},status=status.HTTP_400_BAD_REQUEST)
        try:
            shop_item=ShopItem.objects.get(item_name=item_name,shop=shop)
            return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)
        except ShopItem.DoesNotExist:
            shop_item = ShopItem.objects.create_shopItem(item_name=item_name, image_url=image_url, item_description=item_description, price=price, category=category, shop=shop)
            return Response({'successfully saved': shop_item.item_name})
        except ShopItem.MultipleObjectsReturned:
            shop_item=ShopItem.objects.filter(item_name=item_name,shop=shop).order_by('id').first()
            return Response({"errors": "This data already exists in the database."},status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
"""
    def create(self, request, **kwargs):
        if request.POST.get('datastore'):
            #
        else:
            title=request.POST.get('title')
            username=request.user.username
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            time_type = request.POST.get('time_type')
            try:
                location=save_location(request)['location']
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
                return Response({"errors": "This data already exists in the database."}, status=status.HTTP_400_BAD_REQUEST)
"""

class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
"""
    def create(self, request, **kwargs):
        if request.POST.get('datastore'):
            

        else:
"""

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


"""
    def create(self, request, **kwargs):
        if request.POST.get('datastore'):
            #create
            #check mapping
            #return
        else:
            title=request.POST.get('title')
            username=request.user.username
            description = request.POST.get('description')
            original_id = request.POST.get('original_id')
"""

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

#    def create(self, request, **kwargs):


"""
class TagMappingViewSet(viewsets.ModelViewSet):
    queryset = TagMapping.objects.all()
    serializer_class = TagMappingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

#    def create(self, request, **kwargs):

            #

class DataPictureMappingViewSet(viewsets.ModelViewSet):
    queryset = DataPictureMapping.objects.all()
    serializer_class = DataPictureMappingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

#    def create(self, request, **kwargs):

"""


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


