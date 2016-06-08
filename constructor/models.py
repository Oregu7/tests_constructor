from django.db import models
from users.models import User, Group

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name="Название")
    url = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тема")
    description = models.TextField(blank=True, verbose_name="Описание")
    helps = models.BooleanField(default=False, verbose_name="Подсказки")
    time_completion = models.IntegerField(default=20, verbose_name="Ограничение по времени")
    creator = models.ForeignKey(User, verbose_name="Создатель")
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name="Категория")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    group_access = models.ManyToManyField(Group, blank=True, verbose_name="Групповой доступ")
    two_mark = models.IntegerField(verbose_name="Двойка (до %)")
    three_mark = models.IntegerField(verbose_name="Тройка (до %)")
    four_mark = models.IntegerField(verbose_name="Четверка (до %)")

    def __str__(self):
        return '%s' % self.title

    def get_options(self):
        return Option.objects.filter(test=self, public_access=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

class Query(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    test = models.ForeignKey(Test, verbose_name="Тест")
    help = models.TextField(blank=True, verbose_name="Текст подсказки")
    point = models.IntegerField(default=1, verbose_name="Балл")

    def __str__(self):
        return self.test.title + ' Вопрос #' + str(self.id)

    def get_answers(self):
        answers = Answer.objects.filter(query=self)
        return answers

    def __unicode__(self):
        return self.test.title + ' Вопрос #' + str(self.id)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answer(models.Model):
    query = models.ForeignKey(Query, verbose_name="Вопрос")
    text = models.CharField(max_length=200, blank=True, verbose_name="Текст ответа")
    correct = models.BooleanField(default=False, verbose_name="Правильность ответа")
    analytics = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return "Ответ#%d" % self.id

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class Option(models.Model):
    number = models.IntegerField(default=1, verbose_name="Номер")
    test = models.ForeignKey(Test, verbose_name="Тест")
    questions = models.ManyToManyField(Query, blank=True, verbose_name="Ответы")
    public_access = models.BooleanField(default=False, verbose_name="Публичный доступ")
    time = models.IntegerField(default=0, verbose_name="Ограничения по времени")

    def __str__(self):
        return "Тест#%d Вариант#%d" % (self.test.id, self.number)

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"