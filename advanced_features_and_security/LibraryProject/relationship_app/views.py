from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.generic.detail import DetailView
from .models import Book, Library
from .forms import BookForm


# ---------------------------------------
# Existing Views
# ---------------------------------------


def list_books(request):
    """
    Display list of all books.
    Available to all authenticated users.
    """
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    """
    Display details of a specific library.
    Shows all books in the library.
    """

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------------------------------------
# Authentication Views
# ---------------------------------------


def register(request):
    """
    User registration view.
    Creates new user and logs them in automatically.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# ---------------------------------------
# Role-Based Views
# ---------------------------------------


def is_admin(user):
    """Check if user has Admin role"""
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    """Check if user has Librarian role"""
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    """Check if user has Member role"""
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view.
    Only users with Admin role can access this.
    """
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view.
    Only users with Librarian role can access this.
    """
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view.
    Only users with Member role can access this.
    """
    return render(request, "relationship_app/member_view.html")


# ---------------------------------------
# Permission-Protected Book CRUD Views
# ---------------------------------------


@permission_required("relationship_app.can_view", raise_exception=True)
def view_books(request):
    """
    View all books - requires 'can_view' permission.
    This view is protected and only accessible to users with the can_view permission.
    """
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


@permission_required("relationship_app.can_create", raise_exception=True)
def add_book(request):
    """
    Add a new book - requires 'can_create' permission.
    Only users with can_create permission can access this view.

    Groups with access: Editors, Admins, Librarians
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/add_book.html", {"form": form})


@permission_required("relationship_app.can_edit", raise_exception=True)
def edit_book(request, pk):
    """
    Edit an existing book - requires 'can_edit' permission.
    Only users with can_edit permission can access this view.

    Groups with access: Editors, Admins, Librarians

    Args:
        pk: Primary key of the book to edit
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(
        request, "relationship_app/edit_book.html", {"form": form, "book": book}
    )


@permission_required("relationship_app.can_delete", raise_exception=True)
def delete_book(request, pk):
    """
    Delete a book - requires 'can_delete' permission.
    Only users with can_delete permission can access this view.

    Groups with access: Admins only

    Args:
        pk: Primary key of the book to delete
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})
