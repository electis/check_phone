from django.db import models
from django.contrib.postgres.fields import ArrayField

class Phones(models.Model):
    code = models.PositiveSmallIntegerField(default=0)
    start = models.PositiveIntegerField(default=0)
    finish = models.PositiveIntegerField(default=0)
    numbers = models.PositiveIntegerField(default=0)
    operator = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Settings(models.Model):
    urls = ArrayField(models.CharField(max_length=255), null=True)
    base_ready = models.BooleanField(default=False)
