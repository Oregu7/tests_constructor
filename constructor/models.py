from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    url = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return '%s' % self.name

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    helps = models.BooleanField(default=False)
    time_completion = models.BooleanField(default=False)
    public_access = models.BooleanField(default=False)
    creator = models.ForeignKey(User)
    category = models.ForeignKey(Category, blank=True, null=True)
    questions_count = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    two_mark = models.IntegerField()
    three_mark = models.IntegerField()
    four_mark = models.IntegerField()

    def __str__(self):
        return '%s' % self.title
class Query(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test)
    help = models.TextField(blank=True)
    time = models.IntegerField(default=5)
    point = models.IntegerField(default=1)

    def __str__(self):
        return self.test.title + ' Вопрос #' + str(self.id)

    def get_answers(self):
        answers = Answer.objects.filter(query=self)
        return answers

    def __unicode__(self):
        return self.test.title + ' Вопрос #' + str(self.id)

class Answer(models.Model):
    query = models.ForeignKey(Query)
    text = models.CharField(max_length=200, blank=True)
    correct = models.BooleanField(default=False)
    analytics = models.IntegerField(default=0)

    def __str__(self):
        return "Ответ#%d" % self.id