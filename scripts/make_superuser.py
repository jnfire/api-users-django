from django.contrib.auth.models import User


def run():
    # Delete all admin users
    User.objects.filter(is_superuser=True).delete()

    # Create superuser
    User.objects.create_superuser(
        email="admin@admin.com", username="admin", password="admin"
    )
