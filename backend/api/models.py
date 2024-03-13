from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issubscibed = models.BooleanField(default = False)

class secretkeys(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    secretkey =  models.CharField(max_length=255, blank=True, null=True)


class codes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)