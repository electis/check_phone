from django.db import models
from django.contrib.postgres.fields import ArrayField


class Operator(models.Model):
    operator = models.CharField(max_length=255)


class Location(models.Model):
    location = models.CharField(max_length=255)


class Phones(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    code = models.PositiveSmallIntegerField(default=0, db_index=True)
    start = models.PositiveIntegerField(default=0, db_index=True)
    finish = models.PositiveIntegerField(default=0, db_index=True)
    numbers = models.PositiveIntegerField(default=0)


class Settings(models.Model):
    urls = ArrayField(models.CharField(max_length=255), null=True)
    base_ready = models.BooleanField(default=False)
