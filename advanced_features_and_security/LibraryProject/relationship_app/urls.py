from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    # Book listing (public)
    path("books/", views.list_books, name="list_books"),
    # Library details
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    # Authentication
    path("register/", views.register, name="register"),
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    # Role-Based Views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
    # Permission-Protected Book CRUD Views
    path("books/view/", views.view_books, name="view_books"),  # Requires can_view
    path("books/add/", views.add_book, name="add_book"),  # Requires can_create
    path(
        "books/<int:pk>/edit/", views.edit_book, name="edit_book"
    ),  # Requires can_edit
    path(
        "books/<int:pk>/delete/", views.delete_book, name="delete_book"
    ),  # Requires can_delete
]
