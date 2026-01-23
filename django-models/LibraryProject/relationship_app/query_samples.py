from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Uses ForeignKey relationship.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        # Alternative using related_name:
        # books = author.books.all()
        return books
    except Author.DoesNotExist:
        return None


def list_books_in_library(library_name):
    """
    List all books in a library.
    Uses ManyToMany relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Uses OneToOne relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        # Alternative using related_name:
        # librarian = library.librarian
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Example usage and testing
if __name__ == "__main__":
    # Note: Run this script using Django shell or manage.py shell
    # python manage.py shell < query_samples.py

    print("=" * 50)
    print("Django ORM Query Samples")
    print("=" * 50)

    # Example 1: Query books by author
    print("\n1. Query all books by a specific author:")
    author_name = "J.K. Rowling"
    books = query_books_by_author(author_name)
    if books:
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
    else:
        print(f"No author found with name: {author_name}")

    # Example 2: List books in a library
    print("\n2. List all books in a library:")
    library_name = "Central Library"
    books = list_books_in_library(library_name)
    if books:
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
    else:
        print(f"No library found with name: {library_name}")

    # Example 3: Retrieve librarian for a library
    print("\n3. Retrieve the librarian for a library:")
    library_name = "Central Library"
    librarian = retrieve_librarian_for_library(library_name)
    if librarian:
        print(f"Librarian for {library_name}: {librarian.name}")
    else:
        print(f"No librarian found for library: {library_name}")

    print("\n" + "=" * 50)
