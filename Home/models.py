# from django.conf import settings
from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=10000)
    trials = models.IntegerField(default=10)
    cv_limit = models.IntegerField(default=20)
    ip_address = models.CharField(default="None",max_length=200)
    registerd_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
   