from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField, JSONField


class Location(models.Model):
	place_id = models.BigIntegerField(primary_key=True)
	location_name = models.CharField(max_length=100)
	longitude = models.FloatField()
	latitude = models.FloatField()
	address = models.CharField(max_length=300)
	county_code = models.IntegerField(null=True)
	registered_by = models.CharField(max_length=100)
	registered_at = models.DateTimeField(auto_now_add=True)
	updated_by = models.CharField(max_length=100)
	updated_at = models.DateTimeField(auto_now_add=True)
	boundingbox = ArrayField(models.FloatField(),null=True)
	def __str__(self):
		return '%d: %s'%(self.place_id, self.display_name)


class User(AbstractUser):
	facebook_id = models.BigIntegerField(null=True)
	ownerFlg = models.BooleanField(default=False)
	registered_at = models.DateTimeField(auto_now_add=True)
	location = models.OneToOneField(Location, related_name='user_location')
	def __str__(self):
		return '%d: %s'%(self.id, self.username)


class UserDetail(models.Model):
	user = models.OneToOneField(User, related_name='user_detail')
	phoneNumber = models.IntegerField()
	chime_plan = models.CharField(max_length=50)
	def __str__(self):
		return 'username: %s, first_name: %s, last_name: %s' %(self.username, self.first_name, self.last_name)
	class Meta:
		ordering = ('phoneNumber',)



class Tutor(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	def __str__(self):
		return 'id: %s, first_name: %s, last_name: %s' %(self.id, self.first_name, self.last_name)



class Shop(models.Model):
	shop_name = models.CharField(max_length=200)
	user_editable = models.BooleanField(default=False)
	registered_by = models.CharField(max_length=100)
	registered_at = models.DateTimeField(auto_now_add=True)
	updated_by = models.CharField(max_length=100)
	updated_at = models.DateTimeField(auto_now_add=True)
	shop_owner = models.ForeignKey(User, related_name = "shop_owner",null=True)
	shop_location = models.ForeignKey(Location, related_name = "shop_location",null=True)
	tutor = models.ManyToManyField(Tutor, related_name="tutor")


class Event(models.Model):
	title = models.CharField(max_length=100)
	date = models.DateField(null=True)
	day_of_week = models.IntegerField(null=True)
	start_time = models.TimeField(null=True)
	end_time = models.TimeField(null=True)
	time_type = models.IntegerField()
	registered_by = models.CharField(max_length=100)
	registered_at = models.DateTimeField(auto_now_add=True)
	updated_by = models.CharField(max_length=100)
	updated_at = models.DateTimeField(auto_now_add=True)
	shop = models.ForeignKey(Shop,null=True)
	location = models.ForeignKey(Location, null=True)


class Tag(models.Model):
	tag = models.CharField(max_length=200)
	event = models.ManyToManyField(Event, related_name='event')


class PasswordManager(models.Manager):
    def create_password(self, password=None, facebook_id=None):
    	password = self.create(password=password,facebook_id=facebook_id)


class Password(models.Model):
    password = models.CharField(max_length=100)
    facebook_id = models.BigIntegerField()
    objects = PasswordManager()


class Plan(models.Model):
	user = models.ForeignKey(User, related_name = "user_booking")

