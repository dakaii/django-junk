from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

class LocationManager(models.Manager):
    def create_location(self, location_name=None, longitude=None, latitude=None, address=None, registered_by=None, updated_by=None,boundingbox=None):
    	location = self.create(location_name=location_name, longitude=longitude, latitude=latitude, address=address, registered_by=registered_by, updated_by=updated_by,boundingbox=boundingbox)
    	return location


class Location(models.Model):
	location_name = models.CharField(max_length=100,null=True)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	address = models.CharField(max_length=300,null=True)
	county_code = models.IntegerField(null=True)
	registered_by = models.CharField(max_length=100)
	registered_at = models.DateTimeField(auto_now_add=True)
	updated_by = models.CharField(max_length=100)
	updated_at = models.DateTimeField(auto_now_add=True)
	boundingbox = ArrayField(models.FloatField(),null=True)
	objects = LocationManager()
	def __str__(self):
		return '%d: %s'%(self.id, self.location_name)


class User(AbstractUser):
	facebook_id = models.BigIntegerField(null=True)
	ownerFlg = models.BooleanField(default=False)
	registered_at = models.DateTimeField(auto_now_add=True)
	location = models.OneToOneField(Location, null=True)
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
	updated_by = models.CharField(max_length=100)
	registered_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	shop_owner = models.ForeignKey(User, related_name = "shop_owner",blank=True,null=True)
	shop_location = models.ForeignKey(Location, related_name = "shop_location",blank=True,null=True)
	tutor = models.ManyToManyField(Tutor, related_name="tutor", blank=True)


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
    def create_password(self, password=None, email=None):
    	password = self.create(password=password,email=email)
    	return password


class Password(models.Model):
    password = models.CharField(max_length=100)
    email = models.EmailField()
    objects = PasswordManager()


class Plan(models.Model):
	user = models.ForeignKey(User, related_name = "user_booking")



