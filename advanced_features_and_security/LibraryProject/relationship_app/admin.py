from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile


# ---------------------------------------
# Custom User Admin Configuration
# ---------------------------------------
class CustomUserAdmin(UserAdmin):
    """
    Admin panel configuration for CustomUser.
    Extends the default UserAdmin to include custom fields.
    """

    model = CustomUser

    # Display these fields in the user list view
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )

    # Add filters for these fields
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    # Enable search on these fields
    search_fields = ("username", "email", "first_name", "last_name")

    # Default ordering
    ordering = ("username",)

    # Fieldsets for viewing/editing existing users
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("date_of_birth", "profile_photo"),
                "description": "Extended user information",
            },
        ),
    )

    # Fieldsets for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("date_of_birth", "profile_photo"),
                "description": "Optional: Add date of birth and profile photo",
            },
        ),
    )


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)


# ---------------------------------------
# Other Model Admin Configurations
# ---------------------------------------


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

    # Make it easier to see which user has which role
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")
