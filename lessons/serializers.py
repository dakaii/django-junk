from rest_framework import serializers
from lessons.models import Lesson
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id','lesson_name','description','lesson_detail','timestamp')
