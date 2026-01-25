from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ---------- Existing Models ----------


class Author(models.Model):
    """
    Author model representing a book author.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model with a ForeignKey relationship to Author.
    Each book has one author, but an author can have multiple books.
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title


class Library(models.Model):
    """
    Library model with a ManyToMany relationship to Book.
    A library can have multiple books, and a book can be in multiple libraries.
    """

    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Libraries"


class Librarian(models.Model):
    """
    Librarian model with a OneToOne relationship to Library.
    Each library has exactly one librarian, and each librarian manages one library.
    """

    name = models.CharField(max_length=200)
    library = models.OneToOneField(
        Library, on_delete=models.CASCADE, related_name="librarian"
    )

    def __str__(self):
        return f"{self.name} - {self.library.name}"


# ---------- UserProfile Model for Role-Based Access Control ----------


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ---------- Signals to auto-create UserProfile ----------


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
