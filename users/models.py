from django.db import models
from django.contrib.auth.models import AbstractUser
import string
import random

class Specialization(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    code = models.CharField(max_length=200, primary_key=True, unique=True, verbose_name="Код")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специализацию"
        verbose_name_plural = "Специализации"

class Group(models.Model):

    def generate_secret_code():
        size = 11
        chars = string.ascii_uppercase + string.digits
        while True:
            key = "".join(random.choice(chars) for _ in range(size))
            try:
                Group.objects.get(secret_key=key)
            except Group.DoesNotExist:
               break

        return key

    specialization = models.ForeignKey(Specialization, verbose_name='Специализация')
    name = models.CharField(max_length=250, verbose_name='Название')
    course = models.IntegerField(verbose_name='Курс')
    secret_key = models.CharField(max_length=25, default=generate_secret_code, unique=True, editable=False, verbose_name="Секретный код")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группу"
        verbose_name_plural = "Группы"

class User(AbstractUser):
    study_group = models.ForeignKey(Group, blank=True, null=True, verbose_name='Учебная группа')
    subjects = models.ManyToManyField("constructor.Category", blank=True, verbose_name='Предметы')
