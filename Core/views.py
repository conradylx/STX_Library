import django_filters
import requests
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django_filters import rest_framework, ChoiceFilter, ModelChoiceFilter
from rest_framework import generics

from Core.forms import GeneralBookForm
from Core.models import Book, Language
from Core.serializers import BookSerializer


def get_form_data(request):
    queryset = Book.objects.all()
    languages = Language.objects.all()
    book_title = request.GET.get('book_title')
    book_author = request.GET.get('book_author')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    language = request.GET.get('language')

    if book_title != '' and book_title is not None:
        queryset = queryset.filter(title__icontains=book_title)
    if book_author != '' and book_author is not None:
        queryset = queryset.filter(author__icontains=book_author)
    if book_title != '' and book_title is not None and book_author != '' and book_author is not None:
        queryset = queryset.filter(Q(title__icontains=book_title) | Q(author__name__icontains=book_author)).distinct()
    if date_min != '' and date_min is not None:
        queryset = queryset.filter(published__gte=date_min)
    if date_max != '' and date_max is not None:
        queryset = queryset.filter(published__lte=date_max)
    if language != '' and language != 'Select language' and language is not None:
        queryset = queryset.filter(language__name=language)

    return queryset, languages


def display_data(request):
    queryset, languages = get_form_data(request)

    context = {
        'queryset': queryset,
        'languages': languages,
    }

    return render(request, "index.html", context)


def operations_on_book_function(request, id=0):
    form = GeneralBookForm()
    if id:
        book = get_object_or_404(Book, pk=id)
        form = GeneralBookForm(request.POST or None, instance=book)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('/')
    else:
        if request.method == 'POST':
            form = GeneralBookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'new_book.html', context)


def import_books_from_google_api(request):
    if 'search' in request.GET:
        search = request.GET['search']
        context = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}')
        response = context.json()
        for index in range(len(response["items"])):
            title = response["items"][index]["volumeInfo"]["title"] if 'title' in response["items"][index][
                'volumeInfo'] else "Not given"
            author = response["items"][index]["volumeInfo"]["authors"][0] if 'authors' in response["items"][index][
                'volumeInfo'] else "Not given"
            published = response["items"][index]["volumeInfo"]["publishedDate"] if 'publishedDate' in \
                                                                                   response["items"][index][
                                                                                       'volumeInfo'] else "Not given"

            isbn_number = response["items"][index]["volumeInfo"]["industryIdentifiers"][0][
                "identifier"] if 'industryIdentifiers' in response["items"][index]['volumeInfo'] else "Not given"
            pages = response["items"][index]["volumeInfo"]["pageCount"] if 'pageCount' in response["items"][index][
                'volumeInfo'] else 0
            language = response["items"][index]["volumeInfo"]["language"] if 'language' in \
                                                                             response["items"][index][
                                                                                 'volumeInfo'] else "Not given"
            cover = response["items"][index]["volumeInfo"]["imageLinks"]["thumbnail"] if 'imageLinks' in \
                                                                                         response["items"][index][
                                                                                             'volumeInfo'] else "Not " \
                                                                                                                "given "
            l, is_instance = Language.objects.get_or_create(name=language)
            api_data = Book(title=title, author=author, published=published, isbn_number=isbn_number,
                            pages=pages, language=l, cover=cover)
            print(api_data)
            api_data.save()
        return redirect('/')

    return render(request, 'import_books.html')


class ApiFilter(rest_framework.FilterSet):
    l = tuple(Language.objects.values_list("id", "name"))
    language = django_filters.ChoiceFilter(label='Language', choices=l)

    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'published': ['iexact', 'gte', 'lte'],
        }


class ApiViewSet(generics.ListAPIView):
    model = Book
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = ApiFilter
