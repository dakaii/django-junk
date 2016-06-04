from rest_framework import serializers
from .models import User, Tutor, Schedule, Password
from .models import Location, Event, Shop, Tag, Tutor
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ('id','location_name')


class UserSerializer(serializers.ModelSerializer):
	location = serializers.StringRelatedField()
	class Meta:
	    model = User
	    fields = ('id', 'username','email','location')


class UserDetailSerializer(serializers.ModelSerializer):
	location = serializers.StringRelatedField()
	class Meta:
	    model = User
	    fields = ('id','user','first_name','last_name','email','location')


class TutorSerializer(serializers.ModelSerializer):
	shop = serializers.StringRelatedField(many=True)
	class Meta:
		model = Tutor
		fields = ('id','first_name','last_name','email','shop')


class ShopSerializer(serializers.ModelSerializer):
	shop_owner = serializers.StringRelatedField(many=True)
	shop_location = serializers.StringRelatedField()
	tutor = TutorSerializer(read_only=True, many=True, required=False)
	class Meta:
		model = Shop
		fields = ('id','shop_owner','shop_location','tutor')


class EventSerializer(serializers.ModelSerializer):
	shop = serializers.StringRelatedField()
	location = serializers.StringRelatedField()
	class Meta:
		model = Event
		fields = ('id','title','date','day_of_week','start_time','end_time','time_type','registered_by','registered_at','updated_by','updated_at','shop','location')


class TagSerializer(serializers.ModelSerializer):
	event = serializers.StringRelatedField()
	class Meta:
		model = Tag
		fields = ('id','tag','event')


class ScheduleSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	#event = serializers.StringRelatedField(many=True)
	class Meta:
		model = Schedule
		fields = ('id','user')


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('email', 'password')
        write_only_fields = ('password',)

##-----------------
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        write_only_fields = ('password',)
"""
class SocialSignUpSerializer(serializers.ModelSerializer):
	username = serializers.CharField(read_only=True)
	email = serializers.EmailField(read_only=True)
	class Meta:
		model = User
		fields = ('username', 'email')
        #fields = ('id', 'password')
        #write_only_fields = ('password',)
        """
        