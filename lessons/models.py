from django.db import models


class Lesson(models.Model):
	owner = models.ForeignKey('auth.User',related_name='lessons')
	lesson_name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	lesson_detail = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)

"""
class School(models.Model):
	owner = models.ForeignKey('auth.User',related_name='lessons')
	lesson_name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	lesson_detail = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
"""