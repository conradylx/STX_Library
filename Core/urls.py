from django.urls import path

from Core import views

urlpatterns = [
    path('', views.filter_function, name="index"),
    path('new_book/', views.operations_on_book_function, name='add_book'),
    path('new_book/<int:id>/', views.operations_on_book_function, name='edit_book'),
    path('import_books/', views.import_books_from_google_api, name='import_books'),
]
