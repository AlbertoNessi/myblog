from django.db import models


class Quotes(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100)
    date = models.DateTimeField('publishing date')
    text = models.TextField()
    link = models.CharField(max_length=200)
    author = models.CharField(max_length=100)


class Books(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
