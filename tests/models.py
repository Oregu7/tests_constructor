from django.db import models
from constructor.models import Test
from django.contrib.auth.models import User
# Create your models here.
class Probationer(models.Model):
	test = models.ForeignKey(Test)
	user = models.ForeignKey(User, blank = True, null = True)
	name = models.CharField(max_length=200, blank=True)
	mark = models.IntegerField()
	precent = models.FloatField()
	date = models.DateTimeField(auto_now=True)
