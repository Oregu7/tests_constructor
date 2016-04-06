from django.db import models
from constructor.models import Test

class Country(models.Model):
    name = models.CharField(max_length=200)
    name_translate = models.CharField(max_length=200, default="Страна")
    text = models.TextField()
    translate = models.TextField()
    test = models.ForeignKey(Test)
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name