from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Lesson
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class UserSerializer(serializers.HyperlinkedModelSerializer):
	lessons = serializers.HyperlinkedRelatedField(many=True, view_name='lesson-detail', read_only=True)
	class Meta:
	    model = User
	    fields = ('url', 'username', 'lessons')

class LessonSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	class Meta:
		model = Lesson
		fields = ('url','lesson_name','description','lesson_detail','timestamp','owner')

