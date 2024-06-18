# from django.conf import settings
from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=15)
    registerd_time = models.DateTimeField(default=timezone.now)

   