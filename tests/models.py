from django.db import models
from constructor.models import Test
from users.models import User
# Create your models here.
class Probationer(models.Model):
	test = models.ForeignKey(Test)
	name = models.CharField(max_length=200)
	mark = models.IntegerField()
	precent = models.FloatField()
	date = models.DateTimeField(auto_now=True)
