from rest_framework import serializers
from .models import User, UserDetail, Tutor, Plan, Password
from .models import Location, Event, Shop, Tag, Tutor
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ('id','location_name')


class UserSerializer(serializers.ModelSerializer):
	location = serializers.StringRelatedField(many=True)
	class Meta:
	    model = User
	    fields = ('id', 'username','password','first_name','last_name','email','address','latitude','longitude')


class UserDetailSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField(many=True)
	class Meta:
	    model = UserDetail
	    fields = ('id','user','phoneNumber')


class TutorSerializer(serializers.ModelSerializer):
	shop = serializers.StringRelatedField(many=True)
	class Meta:
		model = Tutor
		fields = ('id','first_name','last_name','email','shop')


class ShopSerializer(serializers.ModelSerializer):
	shop_owner = serializers.StringRelatedField(many=True)
	shop_location = serializers.StringRelatedField(many=True)
	tutor = TutorSerializer(read_only=True, many=True, required=False)
	class Meta:
		model = Shop
		fields = ('id','shop_owner','shop_location','tutor')


class EventSerializer(serializers.ModelSerializer):
	shop = serializers.StringRelatedField(many=True)
	location = serializers.StringRelatedField(many=True)
	class Meta:
		model = Event
		fields = ('id','title','date','day_of_week','start_time','end_time','time_type','registered_by','registered_at','updated_by','updated_at','shop','location')


class TagSerializer(serializers.ModelSerializer):
	event = serializers.StringRelatedField(many=True)
	class Meta:
		model = Tag
		fields = ('id','tag','event')


class PlanSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField(many=True)
	#event = serializers.StringRelatedField(many=True)
	class Meta:
		model = Plan
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
        