from django.db import models
from django.db import models


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


# Create your models here.
