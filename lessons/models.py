from __future__ import unicode_literals

from django.db import models


class Lesson(models.Model):
	lesson_name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	lesson_detail = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
#	class Meta:
#		ordering = ('timestamp',)
