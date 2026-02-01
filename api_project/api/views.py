from rest_framework import generics, viewsets, filters
from .models import Book
from .serializers import BookSerializer


# Original ListAPIView (from Task 1)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Enhanced ViewSet with Search and Filtering (from Task 2)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Adding Search and Ordering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["title", "author"]
