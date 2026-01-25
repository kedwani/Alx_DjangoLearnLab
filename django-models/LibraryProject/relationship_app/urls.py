from django.urls import path
from .views import list_books, LibraryDetailView, RegisterView, LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    # Existing views
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    # Authentication views
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Simple home page (after login)
    path(
        "",
        TemplateView.as_view(template_name="relationship_app/home.html"),
        name="home",
    ),
]
