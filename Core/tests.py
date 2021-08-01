from django.test import TestCase
from django.urls import reverse

from Core.forms import GeneralBookForm
from Core.models import Language, Book
from django.test import Client


class CoreTest(TestCase):

    # models tests
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.add_book_url = reverse('add_book')
        self.edit_book_url = reverse('edit_book', args=[1])
        self.import_books_url = reverse('import_books')
        self.lang = Language.objects.create(name="pl")
        self.book3 = Book.objects.create(title="Book3", author="Author3", published="2020-01-02",
                                         isbn_number="123450089012341",
                                         pages=22,
                                         cover="None", language=Language.objects.get(name="pl"))
        Language.objects.create(name="en")
        Book.objects.create(title="Book", author="Author", published="2020-01-01", isbn_number="123456789012345",
                            pages=21,
                            cover="None", language=Language.objects.get(id=1))
        Book.objects.create(title="Book3", author="Author3", published="2020-01-02", isbn_number="123456789012341",
                            pages=22,
                            cover="None", language=Language.objects.get(id=1))

    def test_language_creation(self):
        language_obj = Language.objects.get(id=1)
        self.assertTrue(isinstance(language_obj, Language))
        self.assertEqual(language_obj.__str__(), language_obj.name)

    def test_book_creation(self):
        book_example = Book.objects.get(title="Book")
        self.assertTrue(isinstance(book_example, Book))
        self.assertEqual(book_example.__str__(), book_example.title)

    # views tests
    def test_get_form_data_func(self):
        lang = Language.objects.get(id=1)
        self.assertQuerysetEqual(list(Book.objects.all()), ['<Book: Book3>', '<Book: Book>', '<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(title__icontains='Book')),
                                 ['<Book: Book3>', '<Book: Book>', '<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(author__icontains='Author')),
                                 ['<Book: Book3>', '<Book: Book>', '<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(published__icontains="2020-01-01")),
                                 ['<Book: Book>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(isbn_number__icontains="123456789012341")),
                                 ['<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(pages__icontains="22")),
                                 ['<Book: Book3>', '<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(cover__icontains="None")),
                                 ['<Book: Book3>', '<Book: Book>', '<Book: Book3>', ], )
        self.assertQuerysetEqual(list(Book.objects.filter(language__exact=lang)),
                                 ['<Book: Book3>', '<Book: Book>', '<Book: Book3>', ], )

    def test_display_data_view_check(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/index.html')

    def test_operations_on_book_function_add_view_check(self):
        response = self.client.get(self.add_book_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/new_book.html')

    def test_operations_on_book_function_add_view_check_id(self):
        response = self.client.get('/new_book/3/')
        self.assertEqual(response.status_code, 200)

    def test_operations_on_book_function_edit_view_check(self):
        response = self.client.get(self.edit_book_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/new_book.html')

    def test_import_books_from_google_api_view_check(self):
        response = self.client.get(self.import_books_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/import_books.html')

    def test_operations_on_book_function_create(self):
        form_data = {'title': "Title4",
                     'author': "Author",
                     'published': "2020-01-01",
                     'isbn_number': "123456789012345",
                     'pages': '21',
                     'cover': "None",
                     'language': Language.objects.get(id=1)}
        GeneralBookForm(data=form_data).save()
        book_saved = Book.objects.get(id=4)
        self.assertEquals(book_saved.title, "Title4")

    def test_form_is_valid(self):
        form_data = {'title': "Title4",
                     'author': "Author",
                     'published': "2020-01-01",
                     'isbn_number': "123456789012345",
                     'pages': '21',
                     'cover': "None",
                     'language': Language.objects.get(id=1)}
        form = GeneralBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form_data = {'title': "",
                     'author': "",
                     'published': "2020-01-01",
                     'isbn_number': "",
                     'pages': '21',
                     'cover': "None",
                     'language': Language.objects.get(id=1)}
        form = GeneralBookForm(data=form_data)
        self.assertFalse(form.is_valid())
