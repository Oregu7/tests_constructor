from django.db import models

# Create your models here.
class Users(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
    	return '%s' % self.login