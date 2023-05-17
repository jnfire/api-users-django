# For user
from django.contrib.auth.models import User
from apps.account.models import Profile
from faker import Faker

# For file
from django.core.files import File
from tempfile import NamedTemporaryFile
import requests
import time
from random import randint


def create_profile(add_image=True):
    fake = Faker("es_ES")

    # Delete all admin users
    User.objects.filter(is_superuser=True).delete()

    # Email
    email = fake.unique.email()

    # Create superuser
    user = User(
        email=email,
        username=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    user.set_password("password")
    user.is_staff = False
    user.save()

    # Create profile
    profile = Profile.objects.create(
        user=user
    )

    if add_image:
        # Add image to profile
        url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
        r = requests.get(url_random_imagen)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        profile.avatar.save(f"random_{int(time.time() * 1000)}.jpg", File(img_temp))

    return profile


def run():
    for _ in range(10):
        create_profile()
