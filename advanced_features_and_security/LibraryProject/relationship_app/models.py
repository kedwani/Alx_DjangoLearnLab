from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# ---------------------------------------
# Author, Book, Library, Librarian
# ---------------------------------------
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model with custom permissions for fine-grained access control.

    Custom Permissions:
    - can_view: Allows viewing books
    - can_create: Allows creating new books
    - can_edit: Allows editing existing books
    - can_delete: Allows deleting books
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="libraries")

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(
        Library, on_delete=models.CASCADE, related_name="librarian"
    )

    def __str__(self):
        return f"{self.name} - {self.library.name}"


# ---------------------------------------
# UserProfile for RBAC
# ---------------------------------------
class UserProfile(models.Model):
    """
    User profile model for role-based access control.
    Automatically created when a CustomUser is created.
    Uses settings.AUTH_USER_MODEL to reference the custom user.
    """

    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Automatically create UserProfile when a new CustomUser is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a CustomUser is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile when the CustomUser is saved.
    """
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
