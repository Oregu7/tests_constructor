from django.db import models
from constructor.models import Test, Answer, Query
import datetime

class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return self.name

class Tested(models.Model):
    role = models.ForeignKey(Role)
    course = models.IntegerField(blank=True, null=True)
    specialization = models.ForeignKey(Specialization, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    test = models.ForeignKey(Test)

    def __str__(self):
        return "Тестируемый %s#%d" % (self.role.name, self.id)

class Analytic(models.Model):
    tested = models.ForeignKey(Tested)
    answer = models.ForeignKey(Answer)
