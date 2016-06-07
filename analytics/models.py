import datetime

from django.db import models

from constructor.models import Test, Answer
from users.models import Specialization


class Role(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

class Tested(models.Model):
    role = models.ForeignKey(Role, verbose_name="Роль")
    course = models.IntegerField(blank=True, null=True, verbose_name="Курс")
    specialization = models.ForeignKey(Specialization, blank=True, null=True, verbose_name="Специализация")
    date = models.DateField(default=datetime.date.today, verbose_name="Дата опроса")
    test = models.ForeignKey(Test, verbose_name="Анкета")

    def get_analytic(self):
        return Analytic.objects.filter(tested=self)

    def __str__(self):
        return "Тестируемый %s#%d" % (self.role.name, self.id)

    class Meta:
        verbose_name = "Опрашиваемого"
        verbose_name_plural = "Опрашиваемые"

class Analytic(models.Model):
    tested = models.ForeignKey(Tested, verbose_name="Опрашиваемый")
    answer = models.ForeignKey(Answer, verbose_name="Ответ")

    class Meta:
        verbose_name = "Ответ опрашиваемого"
        verbose_name_plural = "Ответы опрашиваемых"