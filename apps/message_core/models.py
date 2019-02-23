from django.contrib.auth.models import User
from django.db import models

from apps.common.models import BestPraticesModel


# Create your models here.


class PushToken(BestPraticesModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=200)

    def __str__(self):
        return self.token


class News(BestPraticesModel):
    title = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='news/', null=True, blank=True)
    date = models.DateField()
    place = models.CharField(max_length=20)
    url = models.URLField()

    def __str__(self):
        return "{}".format(self.title)
