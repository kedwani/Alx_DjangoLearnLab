from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters


class BookListView(generics.ListAPIView):
    """Retrieves all books with filtering, searching, and ordering."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_fields = ["title", "author__name", "publication_year"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year"]
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """Retrieves a single book by ID. Read-only for everyone."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """Allows authenticated users to add a new book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """Allows authenticated users to modify an existing book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """Allows authenticated users to remove a book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
