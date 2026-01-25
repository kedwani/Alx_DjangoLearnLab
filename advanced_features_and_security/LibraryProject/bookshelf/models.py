from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ---------------------------------------
# Custom User Manager
# ---------------------------------------
class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    Handles user creation with additional fields.
    """

    def create_user(
        self, username, email, date_of_birth=None, password=None, **extra_fields
    ):
        """
        Create and save a regular user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, date_of_birth=date_of_birth, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password=password, **extra_fields)


# ---------------------------------------
# Custom User Model
# ---------------------------------------
class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Adds date_of_birth and profile_photo fields.
    """

    date_of_birth = models.DateField(
        null=True, blank=True, help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True,
        help_text="User's profile photo",
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def get_age(self):
        """
        Calculate and return the user's age if date_of_birth is set.
        """
        if self.date_of_birth:
            from datetime import date

            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or (
                today.month == self.date_of_birth.month
                and today.day < self.date_of_birth.day
            ):
                age -= 1
            return age
        return None


# ---------------------------------------
# Book Model with Custom Permissions
# ---------------------------------------
class Book(models.Model):
    """
    Book model with custom permissions for fine-grained access control.

    Custom Permissions:
    - can_view: Allows viewing books
    - can_create: Allows creating new books
    - can_edit: Allows editing existing books
    - can_delete: Allows deleting books
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return f"book title is:- {self.title}, author is:-  {self.author}, and publication year is :- {self.publication_year}"
