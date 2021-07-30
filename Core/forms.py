from django import forms
from .models import Book


class GeneralBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published', 'isbn_number', 'pages', 'cover', 'language', ]
