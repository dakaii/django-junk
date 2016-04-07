from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class User(AbstractUser):
	likeCount_lesson = models.IntegerField(default=0)
#	fav_courseID = models.ManyToManyField(Course, related_name='courses')
	ownerFlg = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '%d: %s'%(self.id, self.username)


class UserDetail(models.Model):
	user = models.OneToOneField(User, related_name='user_detail')
	address = models.CharField(max_length=500)
	phoneNumber = models.IntegerField()


class SchoolOwner(models.Model):
	user = models.OneToOneField(User, related_name='school_owner')
	chime_plan = models.CharField(max_length=50)
	def __str__(self):
		return 'username: %s, first_name: %s, last_name: %s' %(self.username, self.first_name, self.last_name)


class School(models.Model):
	school_name = models.CharField(max_length=100)
	school_owner = models.ForeignKey(SchoolOwner, related_name ="school")

	def __str__(self):
		return '%d: %s' %(self.id, self.school_name)
	class Meta:
		ordering = ('school_name',)

class Lesson(models.Model):
	lesson_name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	lesson_detail = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	school = models.ForeignKey(School, related_name = "lesson")

	def __str__(self):
		return self.lesson_name
	class Meta:
		ordering = ('lesson_name',)

class Tutor(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	lessons = models.ManyToManyField(Lesson, related_name="tutor")

	def __str__(self):
		return 'id: %s, first_name: %s, last_name: %s' %(self.id, self.first_name, self.last_name)

class Book(models.Model):
	user = models.ForeignKey(User, related_name = "book_owner")
#	area = models.ForeignKey(Area, related_name='place')

class Area(models.Model):
	areaID = models.CharField(max_length=100)
	area_name = models.CharField(max_length=100)
	parent_areaID = models.IntegerField()
	parent_area_name = models.CharField(max_length=100)





