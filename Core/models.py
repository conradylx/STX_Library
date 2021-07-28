from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published = models.DateField(default=None)
    isbn_number = models.CharField('ISBN', max_length=13)
    pages = models.IntegerField(default=0)
    cover = models.CharField(max_length=200)
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.title
