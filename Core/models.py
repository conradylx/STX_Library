from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    published = models.CharField(max_length=10)
    isbn_number = models.CharField('ISBN', max_length=40)
    pages = models.IntegerField(default=0)
    cover = models.CharField(max_length=200)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
