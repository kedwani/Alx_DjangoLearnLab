book = Book.objects.get(author = "George Orwell")
book.delete()
try :
    book = Book.objects.get(author = "George Orwell")
except:
    print("instance have been deleted succefully.")