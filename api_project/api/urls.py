from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    # Route for the simple ListAPIView
    path("books/", BookList.as_view(), name="book-list"),
    # Include all router-generated CRUD routes
    path("", include(router.urls)),
]
