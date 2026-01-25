from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile


# ---------------------------------------
# Author Admin
# ---------------------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""

    list_display = ("name",)
    search_fields = ("name",)


# ---------------------------------------
# Book Admin with Permission Display
# ---------------------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    Shows custom permissions and allows managing books.
    """

    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title", "author__name")

    # Display information about custom permissions
    fieldsets = (
        ("Book Information", {"fields": ("title", "author")}),
        (
            "Permissions Info",
            {
                "fields": (),
                "description": (
                    "This model has custom permissions: "
                    "can_view, can_create, can_edit, can_delete. "
                    "These permissions are assigned to groups (Viewers, Editors, Admins)."
                ),
            },
        ),
    )


# ---------------------------------------
# Library Admin
# ---------------------------------------
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """Admin interface for Library model."""

    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("books",)


# ---------------------------------------
# Librarian Admin
# ---------------------------------------
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    """Admin interface for Librarian model."""

    list_display = ("name", "library")
    search_fields = ("name", "library__name")


# ---------------------------------------
# UserProfile Admin
# ---------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    Shows user roles for RBAC (Role-Based Access Control).
    """

    list_display = ("user", "role", "get_user_email", "get_user_groups")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")

    def get_user_email(self, obj):
        """Display user's email."""
        return obj.user.email

    get_user_email.short_description = "Email"

    def get_user_groups(self, obj):
        """Display user's groups."""
        return ", ".join([group.name for group in obj.user.groups.all()])

    get_user_groups.short_description = "Groups"

    # Make it easier to see which user has which role
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")

    # Add helpful information
    fieldsets = (
        ("User Profile", {"fields": ("user", "role")}),
        (
            "Information",
            {
                "fields": (),
                "description": (
                    "User roles are used for basic role-based access control. "
                    "For fine-grained permissions, use Groups and Permissions instead. "
                    "Groups: Viewers, Editors, Admins"
                ),
            },
        ),
    )
