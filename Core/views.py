from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from Core.models import Book


def index(request):
    return HttpResponse("Hello")


class BookListView(ListView):
    model = Book
    template_name = "index.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
