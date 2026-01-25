"""
Secure forms implementation for bookshelf app.

Security measures:
1. Input validation using Django forms
2. Field-level validation
3. Custom validators for additional security
4. Sanitization of user inputs
"""

from django import forms
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from .models import Book
import re


# ==============================================================================
# BOOK FORM
# ==============================================================================


class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.

    Security features:
    - Automatic HTML escaping by Django
    - Field validation
    - Type checking
    """

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter book title",
                    "maxlength": "200",  # Prevent excessively long input
                }
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter author name",
                    "maxlength": "100",
                }
            ),
            "publication_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter publication year",
                    "min": "1000",  # Reasonable minimum year
                    "max": "2100",  # Reasonable maximum year
                }
            ),
        }

    def clean_title(self):
        """
        Validate and sanitize book title.

        Security checks:
        - Minimum length requirement
        - Remove excessive whitespace
        - Check for suspicious patterns
        """
        title = self.cleaned_data.get("title")

        if not title:
            raise ValidationError("Title is required.")

        # Remove excessive whitespace
        title = " ".join(title.split())

        # Minimum length validation
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")

        # Check for suspicious patterns (basic XSS attempt detection)
        if re.search(r"<script|javascript:|onerror=|onclick=", title, re.IGNORECASE):
            raise ValidationError("Title contains invalid characters.")

        return title

    def clean_author(self):
        """
        Validate and sanitize author name.
        """
        author = self.cleaned_data.get("author")

        if not author:
            raise ValidationError("Author is required.")

        # Remove excessive whitespace
        author = " ".join(author.split())

        # Minimum length validation
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")

        # Check for suspicious patterns
        if re.search(r"<script|javascript:|onerror=|onclick=", author, re.IGNORECASE):
            raise ValidationError("Author name contains invalid characters.")

        return author

    def clean_publication_year(self):
        """
        Validate publication year.
        """
        year = self.cleaned_data.get("publication_year")

        if year is None:
            raise ValidationError("Publication year is required.")

        # Validate year range
        if year < 1000 or year > 2100:
            raise ValidationError("Publication year must be between 1000 and 2100.")

        return year


# ==============================================================================
# EXAMPLE FORM WITH COMPREHENSIVE VALIDATION
# ==============================================================================


class ExampleForm(forms.Form):
    """
    Example form demonstrating comprehensive security validation.

    This form shows various validation techniques:
    - Built-in validators
    - Custom validators
    - Field-level cleaning
    - Form-level validation
    """

    name = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your name",
            }
        ),
        help_text="Enter your full name (2-100 characters)",
    )

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "your.email@example.com",
            }
        ),
        help_text="Enter a valid email address",
    )

    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your age",
            }
        ),
        help_text="Optional: Enter your age (0-150)",
    )

    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your message",
                "rows": 5,
            }
        ),
        help_text="Enter your message (max 1000 characters)",
    )

    agree_to_terms = forms.BooleanField(
        required=True,
        error_messages={"required": "You must agree to the terms and conditions."},
    )

    def clean_name(self):
        """
        Validate and sanitize name field.

        Security checks:
        - Remove excessive whitespace
        - Check for suspicious patterns
        - Validate character content
        """
        name = self.cleaned_data.get("name")

        # Remove excessive whitespace
        name = " ".join(name.split())

        # Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError(
                "Name can only contain letters, spaces, hyphens, and apostrophes."
            )

        # Check for XSS attempts
        if re.search(r"<|>|&lt;|&gt;|javascript:|onerror=", name, re.IGNORECASE):
            raise ValidationError("Name contains invalid characters.")

        return name

    def clean_email(self):
        """
        Additional email validation beyond EmailValidator.
        """
        email = self.cleaned_data.get("email")

        # Convert to lowercase for consistency
        email = email.lower()

        # Additional domain validation (example)
        domain = email.split("@")[-1]
        blocked_domains = ["tempmail.com", "throwaway.email"]

        if domain in blocked_domains:
            raise ValidationError("Email from this domain is not allowed.")

        return email

    def clean_message(self):
        """
        Validate and sanitize message content.
        """
        message = self.cleaned_data.get("message")

        # Remove excessive whitespace while preserving line breaks
        message = re.sub(r"[ \t]+", " ", message)
        message = re.sub(r"\n\s*\n", "\n\n", message)

        # Check for spam-like patterns
        if message.count("http://") + message.count("https://") > 5:
            raise ValidationError("Message contains too many links.")

        # Check for suspicious patterns
        if re.search(r"<script|javascript:|onerror=|onclick=", message, re.IGNORECASE):
            raise ValidationError("Message contains invalid content.")

        return message

    def clean(self):
        """
        Form-level validation.

        This runs after all field-level cleaning.
        Use for validations that involve multiple fields.
        """
        cleaned_data = super().clean()

        # Example: Cross-field validation
        age = cleaned_data.get("age")
        agree_to_terms = cleaned_data.get("agree_to_terms")

        if age is not None and age < 13 and agree_to_terms:
            raise ValidationError(
                "Users under 13 cannot agree to terms without parental consent."
            )

        return cleaned_data


# ==============================================================================
# SEARCH FORM (For Secure Searching)
# ==============================================================================


class BookSearchForm(forms.Form):
    """
    Secure search form for books.

    Security features:
    - Input validation
    - Length limits
    - XSS prevention
    """

    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search books...",
                "maxlength": "200",
            }
        ),
    )

    def clean_search(self):
        """
        Validate and sanitize search query.
        """
        search = self.cleaned_data.get("search", "")

        # Remove excessive whitespace
        search = " ".join(search.split())

        # Limit search term length
        if len(search) > 200:
            search = search[:200]

        # Remove potentially dangerous characters
        # Allow only alphanumeric, spaces, and common punctuation
        search = re.sub(r"[^\w\s\-\']", "", search)

        return search
