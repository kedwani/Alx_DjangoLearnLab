from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser


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
# Book Admin Configuration
# ---------------------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("title", "author", "publication_year")
    search_fields = ("title", "author", "publication_year")
