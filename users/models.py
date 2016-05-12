from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

class Specialization(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, primary_key=True, unique=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    specialization = models.ForeignKey(Specialization, verbose_name='Специализация')
    name = models.CharField(max_length=250, verbose_name='Название')
    course = models.IntegerField(verbose_name='Курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группу"
        verbose_name_plural = "Группы"

class User(AbstractUser):
    study_group = models.ForeignKey(Group, blank=True, null=True, verbose_name='Учебная группа')
    subjects = models.ManyToManyField(Subject, blank=True, verbose_name='Предметы')
