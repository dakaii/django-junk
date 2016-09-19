from rest_framework import serializers
from .models import User, Tutor, Schedule
from .models import Location, Event, Shop, Tag, Tutor, Course
#from .models import TagMapping, DataPictureMapping
from . models import ShopItem


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'location_name')


class TutorSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tutor
        fields = ('id', 'first_name', 'last_name', 'email', 'shop')


class EventSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    class Meta:
        model = Event
        fields = ('id', 'title', 'date','day_of_week','start_time','end_time','time_type','registered_by','registered_at','updated_by','updated_at','shop','location')


class TagSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields = ('id','tag','event')


class ScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Schedule
        fields = ('id')


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('id', 'first_name', 'last_name', 'email')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title')

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ('id', 'item_name','category','image_url','item_description','price')


class ShopSerializer(serializers.ModelSerializer):
#    shop_owner = serializers.StringRelatedField(many=True)
    shop_owner = serializers.StringRelatedField()
#    shop_location = serializers.StringRelatedField()
    shop_item = ShopItemSerializer(many=True)
    class Meta:
        model = Shop
        fields = ('id', 'shop_name', 'shop_owner', 'shop_location', 'cuisine_type','shop_item')


"""
class TagMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMapping
        fields = ('id', 'name')

class DataPictureMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPictureMapping
        fields = ('id', 'name')
"""

class ShopItemSerializer(serializers.ModelSerializer):
#    shop_item = serializers.StringRelatedField()
    class Meta:
        model = ShopItem
        fields = ('id','item_name','image_url','item_description','price')


class UserSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'username','email','location')


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','location')


#--------------------
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        write_only_fields = ('password',)
