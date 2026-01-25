from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile


# ---------------------------------------
# Custom User Admin Configuration
# ---------------------------------------
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    Extends the default UserAdmin to include custom fields.
    """

    model = CustomUser

    # Fields to display in the user list
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
    )

    # Fields to filter by in the sidebar
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    # Fields to search by
    search_fields = ("username", "email", "first_name", "last_name")

    # Order by username
    ordering = ("username",)

    # Fieldsets for editing existing users
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": ("date_of_birth", "profile_photo"),
                "description": "Additional user profile information",
            },
        ),
    )

    # Fieldsets for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": ("date_of_birth", "profile_photo"),
                "description": "Optional additional information",
            },
        ),
    )


# ---------------------------------------
# Register Models
# ---------------------------------------
admin.site.register(CustomUser, CustomUserAdmin)


# Optional: Register other models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title", "author__name")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("books",)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name", "library")
    search_fields = ("name", "library__name")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")
