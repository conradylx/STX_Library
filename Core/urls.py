from django.urls import path

from Core import views
from Core.views import ApiViewSet

urlpatterns = [
    path('', views.display_data, name="index"),
    path('new_book/', views.operations_on_book_function, name='add_book'),
    path('new_book/<int:id>/', views.operations_on_book_function, name='edit_book'),
    path('import_books/', views.import_books_from_google_api, name='import_books'),
    path('api/', ApiViewSet.as_view(), name='api_view')
]
