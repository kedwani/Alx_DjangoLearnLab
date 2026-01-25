"""
Setup script to create groups and assign permissions.

Run this script using Django shell:
    python manage.py shell < setup_permissions.py

Or manually in Django shell:
    python manage.py shell
    >>> exec(open('setup_permissions.py').read())

This script creates three groups with appropriate permissions:
1. Viewers - Can only view books
2. Editors - Can view, create, and edit books
3. Admins - Can view, create, edit, and delete books
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book


def setup_groups_and_permissions():
    """
    Create groups and assign permissions for the Book model.
    """
    print("=" * 60)
    print("Setting up Groups and Permissions")
    print("=" * 60)

    # Get the content type for the Book model
    book_content_type = ContentType.objects.get_for_model(Book)

    # Get or create all permissions
    can_view, _ = Permission.objects.get_or_create(
        codename="can_view",
        name="Can view book",
        content_type=book_content_type,
    )
    can_create, _ = Permission.objects.get_or_create(
        codename="can_create",
        name="Can create book",
        content_type=book_content_type,
    )
    can_edit, _ = Permission.objects.get_or_create(
        codename="can_edit",
        name="Can edit book",
        content_type=book_content_type,
    )
    can_delete, _ = Permission.objects.get_or_create(
        codename="can_delete",
        name="Can delete book",
        content_type=book_content_type,
    )

    print("\n✓ Permissions created/verified:")
    print(f"  - {can_view.name}")
    print(f"  - {can_create.name}")
    print(f"  - {can_edit.name}")
    print(f"  - {can_delete.name}")

    # Create Groups and assign permissions

    # 1. Viewers Group - Can only view books
    viewers_group, created = Group.objects.get_or_create(name="Viewers")
    viewers_group.permissions.clear()  # Clear existing permissions
    viewers_group.permissions.add(can_view)
    print(f"\n✓ {'Created' if created else 'Updated'} 'Viewers' group")
    print(f"  Permissions: can_view")

    # 2. Editors Group - Can view, create, and edit books
    editors_group, created = Group.objects.get_or_create(name="Editors")
    editors_group.permissions.clear()
    editors_group.permissions.add(can_view, can_create, can_edit)
    print(f"\n✓ {'Created' if created else 'Updated'} 'Editors' group")
    print(f"  Permissions: can_view, can_create, can_edit")

    # 3. Admins Group - Full access (view, create, edit, delete)
    admins_group, created = Group.objects.get_or_create(name="Admins")
    admins_group.permissions.clear()
    admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
    print(f"\n✓ {'Created' if created else 'Updated'} 'Admins' group")
    print(f"  Permissions: can_view, can_create, can_edit, can_delete")

    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Create test users in Django admin")
    print("2. Assign users to groups")
    print("3. Test permissions by logging in as different users")
    print("\nTo assign a user to a group programmatically:")
    print("  user.groups.add(viewers_group)")
    print("  user.groups.add(editors_group)")
    print("  user.groups.add(admins_group)")
    print("=" * 60)


# Run the setup
if __name__ == "__main__":
    setup_groups_and_permissions()
else:
    # If imported or run from shell
    setup_groups_and_permissions()
