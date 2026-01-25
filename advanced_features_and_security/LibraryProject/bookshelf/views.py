from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from django import forms


# ---------------------------------------
# Book Form
# ---------------------------------------
class BookForm(forms.ModelForm):
    """Form for creating and editing books."""

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "publication_year": forms.NumberInput(attrs={"class": "form-control"}),
        }


# ---------------------------------------
# Permission-Protected Views
# ---------------------------------------


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    View all books - requires 'can_view' permission.
    This view is protected and only accessible to users with the can_view permission.

    Groups with access: Viewers, Editors, Admins
    """
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """
    Create a new book - requires 'can_create' permission.
    Only users with can_create permission can access this view.

    Groups with access: Editors, Admins
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(
        request, "bookshelf/book_form.html", {"form": form, "action": "Create"}
    )


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book - requires 'can_edit' permission.
    Only users with can_edit permission can access this view.

    Groups with access: Editors, Admins

    Args:
        pk: Primary key of the book to edit
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(
        request,
        "bookshelf/book_form.html",
        {"form": form, "action": "Edit", "book": book},
    )


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
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
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
