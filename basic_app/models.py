from django.db import models

# Create your models here.

class usersignup(models.Model):
    username = models.CharField(max_length = 100)
    pswd = models.CharField(max_length = 100)

class userlogin(models.Model):
    username = models.CharField(max_length = 100)
    pswd = models.CharField(max_length = 100)

'''
class getNifty50(models.Model):
   getNifty50 = models.CharField(max_length = 10000)
'''

class Meta :
    db_table = "user"