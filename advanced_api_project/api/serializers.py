from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """Serializes all book fields and validates the publication year."""

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes author name and dynamically nests their related books."""

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]
