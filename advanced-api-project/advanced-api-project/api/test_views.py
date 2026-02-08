from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter", publication_year=1997, author=self.author
        )
        self.list_url = reverse("book-list")

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password")
        data = {
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": self.author.id,
        }
        response = self.client.post(reverse("book-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_books_by_year(self):
        response = self.client.get(self.list_url, {"publication_year": 1997})
        self.assertEqual(len(response.data), 1)

    def test_delete_book_unauthenticated(self):
        url = reverse("book-delete", kwargs={"pk": self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
