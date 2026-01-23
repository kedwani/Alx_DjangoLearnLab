from django.urls import path
from . import views

urlpatterns = [
    # Function-based view URL pattern
    path("books/", views.list_books, name="list_books"),
    # Class-based view URL pattern
    # The <int:pk> captures the library's primary key from the URL
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
]
