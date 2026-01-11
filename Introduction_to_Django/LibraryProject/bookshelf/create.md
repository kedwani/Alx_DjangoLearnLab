# Creating a Book Object

You can create a new book record in the database using Django ORM.

## Example


from bookshelf.models import Book

Book.objects.create(
    title="Clean Code",
    author="Robert C. Martin",
    publication_year=2008
)


