from django.db import models


class Author(models.Model):
    """Model representing an author with a name field."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book with title, year, and author relationship."""

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
