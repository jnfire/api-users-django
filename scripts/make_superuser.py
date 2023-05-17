# For user
from django.contrib.auth.models import User
from apps.account.models import Profile

# For file
from django.core.files import File
from tempfile import NamedTemporaryFile
import requests
import time
from random import randint


def run():
    # Delete all admin users
    User.objects.filter(is_superuser=True).delete()

    # Create superuser
    user = User.objects.create_superuser(
        email="admin@admin.com", username="admin", password="admin"
    )

    # Create profile
    profile = Profile.objects.create(
        user=user
    )

    # Add image to profile
    url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
    r = requests.get(url_random_imagen)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()
    profile.avatar.save(f"random_{int(time.time() * 1000)}.jpg", File(img_temp))
