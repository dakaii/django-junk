from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PasswordManager(models.Manager):
    def create_password(self, password=None, email=None):
        password = self.create(password=password,email=email)
        return password


class Password(models.Model):
    password = models.CharField(max_length=100)
    email = models.EmailField()
    objects = PasswordManager()


class LocationManager(models.Manager):
    def create_location(self, location_name=None, original_id=None, access=None, city=None, state=None, zipcode=None, longitude=None, latitude=None, address=None, country_code=None, registered_by=None, updated_by=None):
        location = self.create(location_name=location_name, original_id=original_id, access=access, city=city, state=state, zipcode=zipcode, longitude=longitude, latitude=latitude, address=address, country_code=country_code, registered_by=registered_by, updated_by=updated_by)
        return location


class Location(models.Model):
    location_name = models.CharField(max_length=100,null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    original_id = models.CharField(max_length=100, null=True, blank=True)
    direction = models.CharField(max_length=300, null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=5,null=True,blank=True)
    zipcode = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=300)
    country_code = models.CharField(max_length=5,null=True,blank=True)
    registered_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = LocationManager()

    def __str__(self):
        return '%d: %s'%(self.id, self.location_name)


class User(AbstractUser):
    facebook_id = models.BigIntegerField(null=True)
    ownerFlg = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    location = models.OneToOneField(Location, null=True)
    phoneNumber = models.IntegerField(null=True)
    qro_plan = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '%d: %s'%(self.id, self.username)


class TutorManager(models.Manager):
    def create_tutor(self, first_name=None, last_name=None, email=None):
        tutor = self.create(first_name=first_name, last_name=last_name, email=email)
        return tutor


class Tutor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return 'id: %s, first_name: %s, last_name: %s' %(self.id, self.first_name, self.last_name)


class ShopManager(models.Manager):
    def create_shop(self, shop_name=None,cuisine_type=None,referUrl=None,tel=None, registered_by=None, updated_by=None, shop_owner=None, shop_location=None):
#        shop = self.create(shop_name=shop_name, user_editable=user_editable, registered_by=registered_by, updated_by=updated_by, shop_owner=shop_owner, shop_location=shop_location)
        shop = self.create(shop_name=shop_name, cuisine_type=cuisine_type, referUrl=referUrl, tel=tel, registered_by=registered_by, updated_by=updated_by, shop_owner=shop_owner, shop_location=shop_location)
        return shop


class Shop(models.Model):
    shop_name = models.CharField(max_length=200)
    cuisine_type = models.CharField(max_length=50)
#    user_editable = models.BooleanField(default=False)
#    original_id = models.BigIntegerField(null=True, blank=True)
#    floor = models.CharField(max_length=25, null=True, blank=True)
    referUrl = models.URLField(null=True, blank=True)
#    remarks = models.CharField(max_length=25, null=True, blank=True)
    tel = models.CharField(max_length=12,null=True,blank=True)
    registered_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    shop_owner = models.ForeignKey(User, related_name="shop_owner", on_delete=models.CASCADE)
    shop_location =  models.CharField(max_length=100)
    #shop_location = models.ForeignKey(Location, related_name="shop_location", on_delete=models.CASCADE)
#    shop_item = models.ForeignKey(ShopItem, related_name="shop_item", on_delete=models.CASCADE)
    objects = ShopManager()


class CourseManager(models.Manager):
    def create_course(self, title=None, original_id=None, description=None, registered_by=None, registered_at=None, updated_by=None, updated_at=None):
        course = self.create(title=title,original_id=original_id,description=description,registered_by=registered_by,registered_at=registered_at,updated_by=updated_by,updated_at=updated_at)
        return course


class Course(models.Model):
    title = models.CharField(max_length=200)
    original_id = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length = 500)
    registered_by = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now_add=True)


class EventManager(models.Manager):
    def create_event(self, title=None, date=None, day_of_week=None, start_time=None, end_time=None, time_type=None, registered_by=None, updated_by=None, shop=None, location=None):
        event = self.create(title=title, date=date, day_of_week=day_of_week, start_time=start_time, end_time=end_time, time_type=time_type, registered_by=registered_by, updated_by=updated_by, shop=shop, location=location)
        return event


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    #day_of_week= ArrayField(models.BooleanField(default=False), blank=True, size=7)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    time_type = models.IntegerField()
    registered_by = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)
    shop = models.ForeignKey(Shop,null=True,blank=True)
    course = models.ForeignKey(Course,null=True,blank=True, on_delete=models.CASCADE)
    tutorKey = models.ManyToManyField(Tutor, related_name="tutor",blank=True)
    tutorName = models.CharField(max_length=20,null=True,blank=True)
    objects = EventManager()


class TagManager(models.Manager):
    def create_tag(self, tag=None, dataID=None, registered_by=None, registered_at=None, updated_by=None, updated_at=None, event=None):
        event = self.create(tag=tag, dataID=dataID, registered_by=registered_by, registered_at=registered_at, updated_by=updated_by, updated_at=updated_at, event=event)
        return event


class Tag(models.Model):
    tag = models.CharField(max_length=200)
    dataID = models.CharField(max_length=200)
    registered_by = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now_add=True)
    event = models.ManyToManyField(Event, related_name='event')
    objects = TagManager()


class ScheduleManager(models.Manager):
    def create_schedule(self, user=None):
        schedule = self.create(user=user)
        return schedule


class Schedule(models.Model):
    user = models.ForeignKey(User, related_name = "user_booking", on_delete=models.CASCADE)


class ShopItemManager(models.Manager):
    def create_shopItem(self, item_name=None, image_url = None, item_description = None, price = None,category=None,shop=None):
        shop_item = self.create(item_name=item_name, image_url=image_url, item_description=item_description, price=price, category=category,shop=shop)
        return shop_item


class ShopItem(models.Model):
    item_name = models.CharField(max_length=300)
    image_url = models.URLField(null=True, blank=True)
    item_description = models.CharField(max_length = 500,null=True, blank=True)
    price = models.CharField(max_length = 500,null=True, blank=True)
    category = models.CharField(max_length=500,null=True, blank=True)
    shop = models.ForeignKey(Shop, related_name="shop_item", on_delete=models.CASCADE)
    objects = ShopItemManager()

    class Meta:
        #unique_together = ('album', 'order')
        ordering = ['category']
    
    def __str__(self):
        data = dict()
        data['category'] = self.category
        data['item_name'] = self.item_name
        data['item_description'] = self.item_description
        data['price'] = self.price
        data['image_url'] = self.image_url
        return json.dumps(data)
        #return '%s: %s' % (self.item_name, self.category)


class Category(models.Model):
    name = models.CharField(max_length=300)







