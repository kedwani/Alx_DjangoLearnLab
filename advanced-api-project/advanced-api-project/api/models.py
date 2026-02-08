from django.db import models


class Author(models.Model):
    """Stores author names. One author can have many books."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Stores book details linked to an author via a ForeignKey."""

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
