from rest_framework import serializers
from .models import User, UserDetail,SchoolOwner, School, Lesson, Tutor, Booking, Password
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class UserSerializer(serializers.ModelSerializer):
	class Meta:
	    model = User
	    fields = ('id', 'username','password','first_name','last_name','email','likeCount_lesson')


class UserDetailSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField(many=True)
	class Meta:
	    model = UserDetail
	    fields = ('user','address')


class SchoolOwnerSerializer(serializers.ModelSerializer):
	school = serializers.StringRelatedField(many=True)
	class Meta:
		model = SchoolOwner
		fields = ('id', 'username','password','email','school')


class SchoolSerializer(serializers.ModelSerializer):
	lesson = serializers.StringRelatedField(many=True)
	class Meta:
		model = School
		fields = ('id', 'school_owner','school_name','lesson')


class LessonSerializer(serializers.ModelSerializer):
	tutor = serializers.StringRelatedField(many=True)
	class Meta:
		model = Lesson
		fields = ('id','lesson_name','tutor','description','lesson_detail','timestamp')

class BookingSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField(many=True)
	lesson = serializers.StringRelatedField(many=True)

	class Meta:
		model = Booking
		fields = ('id',)

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('password', 'facebook_id')
        #write_only_fields = ('password','facebook_id')

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
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
        