from django.db import models

from constructor.models import Test, Answer, Option
from users.models import User

# Create your models here.
class Probationer(models.Model):
    option = models.ForeignKey(Option, verbose_name="Вариант")
    user = models.ForeignKey(User, verbose_name="Тестируемый")
    mark = models.IntegerField(verbose_name="Отметка")
    precent = models.FloatField(verbose_name="Процент")
    date = models.DateTimeField(verbose_name="Дата")

    def get_answers(self):
        return ProbationerAnswer.objects.filter(probationer=self)

    class Meta:
        verbose_name = "Тестируемого"
        verbose_name_plural = "Тестируемые"

class ProbationerAnswer(models.Model):
    probationer = models.ForeignKey(Probationer, verbose_name="Тестируемый")
    answer = models.ForeignKey(Answer, verbose_name="Ответ")

    class Meta:
        verbose_name = "Ответ Тестируемого"
        verbose_name_plural = "Ответы Тестируемых"
