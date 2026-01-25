"""
Secure views implementation for bookshelf app.

Security measures implemented:
1. Use Django ORM to prevent SQL injection
2. Validate and sanitize all user inputs using forms
3. Use CSRF tokens in all forms
4. Escape output to prevent XSS
5. Use permission decorators for access control
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.utils.html import escape
from .models import Book
from .forms import BookForm, ExampleForm
import logging

# Set up logging for security events
logger = logging.getLogger(__name__)


# ==============================================================================
# SECURE BOOK CRUD VIEWS
# ==============================================================================


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Display list of all books with secure search functionality.

    Security measures:
    - Uses Django ORM to prevent SQL injection
    - Sanitizes search input
    - Validates user permissions
    """
    books = Book.objects.all()

    # Secure search functionality
    search_query = request.GET.get("search", "")
    if search_query:
        # Sanitize search input by escaping HTML
        search_query = escape(search_query)

        # Use Django ORM with Q objects - prevents SQL injection
        # NEVER use raw SQL with string formatting: f"SELECT * FROM books WHERE title='{search_query}'"
        books = books.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )

        # Log search for security monitoring
        logger.info(f"Book search performed: {search_query}")

    context = {
        "books": books,
        "search_query": search_query,
    }
    return render(request, "bookshelf/book_list.html", context)


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """
    Create a new book with secure form handling.

    Security measures:
    - Uses Django forms for input validation and sanitization
    - CSRF token required (enforced by middleware)
    - Permission check before allowing access
    """
    if request.method == "POST":
        # Use Django forms to validate and sanitize input
        # This prevents XSS and ensures data integrity
        form = BookForm(request.POST)

        if form.is_valid():
            # Form validation ensures data is safe
            book = form.save()

            # Log the creation for audit trail
            logger.info(f"Book created: {book.title} by user: {request.user.username}")

            return redirect("book_list")
        else:
            # Log validation failures for security monitoring
            logger.warning(
                f"Invalid book creation attempt by user: {request.user.username}"
            )
    else:
        form = BookForm()

    context = {"form": form, "action": "Create"}
    return render(request, "bookshelf/book_form.html", context)


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book with secure handling.

    Security measures:
    - Uses get_object_or_404 to prevent information disclosure
    - Form validation for all inputs
    - Permission verification

    Args:
        pk: Primary key of the book (validated by Django URL routing)
    """
    # get_object_or_404 prevents information disclosure
    # Returns 404 instead of revealing whether object exists
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            updated_book = form.save()
            logger.info(
                f"Book updated: {updated_book.title} by user: {request.user.username}"
            )
            return redirect("book_list")
        else:
            logger.warning(
                f"Invalid book update attempt for ID {pk} by user: {request.user.username}"
            )
    else:
        form = BookForm(instance=book)

    context = {"form": form, "action": "Edit", "book": book}
    return render(request, "bookshelf/book_form.html", context)


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book with confirmation.

    Security measures:
    - Requires POST request for state-changing operation
    - CSRF token protection
    - Permission verification
    - Audit logging
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book_title = book.title
        book.delete()

        # Log deletion for audit trail
        logger.info(f"Book deleted: {book_title} by user: {request.user.username}")

        return redirect("book_list")

    context = {"book": book}
    return render(request, "bookshelf/book_confirm_delete.html", context)


# ==============================================================================
# EXAMPLE: INSECURE VS SECURE APPROACHES
# ==============================================================================


def insecure_search_example(request):
    """
    EXAMPLE OF WHAT NOT TO DO - SQL Injection Vulnerability

    This function demonstrates an INSECURE approach.
    DO NOT USE THIS IN PRODUCTION!
    """
    # VULNERABLE TO SQL INJECTION - NEVER DO THIS!
    # search = request.GET.get('search', '')
    # raw_query = f"SELECT * FROM bookshelf_book WHERE title LIKE '%{search}%'"
    # books = Book.objects.raw(raw_query)

    # An attacker could input: ' OR '1'='1
    # Resulting query: SELECT * FROM bookshelf_book WHERE title LIKE '%' OR '1'='1%'
    # This would return all books regardless of search term

    pass


def secure_search_example(request):
    """
    EXAMPLE OF SECURE APPROACH

    Always use Django ORM with parameterized queries.
    """
    search = request.GET.get("search", "")

    # SECURE - Django ORM automatically escapes parameters
    books = Book.objects.filter(title__icontains=search)

    # If you MUST use raw SQL, use parameterization:
    # books = Book.objects.raw('SELECT * FROM bookshelf_book WHERE title LIKE %s', ['%' + search + '%'])

    return render(request, "bookshelf/book_list.html", {"books": books})


# ==============================================================================
# FORM EXAMPLE VIEW
# ==============================================================================


@login_required
def form_example_view(request):
    """
    Example view demonstrating secure form handling.

    Security measures:
    - CSRF token required
    - Form validation
    - Input sanitization via Django forms
    - XSS prevention through template auto-escaping
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)

        if form.is_valid():
            # Access cleaned, validated data
            # Django forms automatically escape HTML to prevent XSS
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Process the data safely
            # All data has been validated and sanitized
            logger.info(f"Form submitted by {email}")

            # Redirect after POST to prevent duplicate submissions
            return redirect("form_success")
    else:
        form = ExampleForm()

    context = {"form": form}
    return render(request, "bookshelf/form_example.html", context)
