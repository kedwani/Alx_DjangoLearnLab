from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view to list all books
def list_books(request):
    """
    Function-based view that retrieves all books from the database
    and renders them in a template.
    """
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "relationship_app/list_books.html", context)


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    including all books available in that library.
    Uses Django's generic DetailView.
    """

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        """
        Override to add additional context if needed.
        The library object is automatically available as 'library' in the template.
        """
        context = super().get_context_data(**kwargs)
        # Additional context can be added here if needed
        # For example: context['total_books'] = self.object.books.count()
        return context
