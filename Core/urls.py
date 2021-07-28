from django.urls import path

from Core import views
from Core.views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name="index"),
]
