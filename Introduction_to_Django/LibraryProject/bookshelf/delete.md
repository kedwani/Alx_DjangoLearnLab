from bookshelf.modles import Book
book = Book.objects.get(author = "George Orwell")
book.delete()
books = Book.objects.all()
print(books)
try :
    book = Book.objects.get(author = "George Orwell")
except:
    print("instance have been deleted succefully.")