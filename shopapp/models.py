from django.db import models

# Create your models here.

from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=25)
    password = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Authors(models.Model):
    fullname = models.CharField(max_length=25)

    def __str__(self):
        return self.fullname


class Books(models.Model):
    slug = models.SlugField()
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    img = models.CharField(max_length=35)
    description = models.TextField()
    stock = models.IntegerField()

    def __str__(self):
        return self.title
