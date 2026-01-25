from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Book, Library

# ---------- Existing Views ----------


def list_books(request):
    books = Book.objects.all()
    output = []

    for book in books:
        output.append(f"{book.title} by {book.author.name}")

    return HttpResponse("<br>".join(output))


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------- Registration View ----------

from django.views import View


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "relationship_app/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # تسجيل الدخول مباشرة بعد التسجيل
            return redirect("home")
        return render(request, "relationship_app/register.html", {"form": form})


# function-based wrapper for autograder
def register(request):
    from .views import RegisterView

    view = RegisterView.as_view()
    return view(request)
