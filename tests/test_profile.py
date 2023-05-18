from django.urls import reverse
import pytest
from scripts.make_users import create_profile
from core.settings import MEDIA_ROOT

# Files
import base64
from random import randint
import requests
import os


def get_random_image_on_base64():
    """Get random image on base64"""
    url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
    r = requests.get(url_random_imagen)
    return base64.b64encode(r.content).decode("utf-8")


def remove_test_images():
    """Remove all images created in test"""

    folder_path = f"{MEDIA_ROOT}/avatar_images/"

    # Get all files in folder
    for filename in os.listdir(folder_path):
        if "_test." in filename:
            # File route
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


@pytest.mark.django_db
def test_get_profile(client):
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ),
    )
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Get profile
    response = client.get(
        reverse("profile"),
        HTTP_AUTHORIZATION=f" Token {token}",
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "name" in content and content.get("name") == profile.name
    ), f"Profile not found in response: {content}"
    assert (
        "email" in content and content.get("email") == profile.user.email
    ), f"Profile not found in response: {content}"
    assert (
        "first_name" in content and content.get("first_name") == profile.user.first_name
    ), f"Profile not found in response: {content}"
    assert (
        "last_name" in content and content.get("last_name") == profile.user.last_name
    ), f"Profile not found in response: {content}"


@pytest.mark.django_db
def test_get_profile_error_not_send_token(client):
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ),
    )
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Get profile
    response = client.get(
        reverse("profile"),
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 401
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "detail" in content
        and content.get("detail")
        == "Las credenciales de autenticación no se proveyeron."
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_get_profile_error_invalid_token(client):
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ),
    )
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Get profile
    response = client.get(
        reverse("profile"),
        HTTP_AUTHORIZATION=f" Token {token}invalid",
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 401
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "detail" in content and content.get("detail") == "Token inválido."
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_update_profile(client):
    # Given
    profile = create_profile()

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ),
    )
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Update profile
    response = client.put(
        reverse("profile"),
        data=dict(
            email="test@test.com",
            first_name="New first name",
            last_name="New last name",
            avatar=dict(
                name="test.jpg",
                base64=get_random_image_on_base64(),
            ),
        ),
        content_type="application/json",
        HTTP_AUTHORIZATION=f" Token {token}",
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"

    # When
    # Get profile
    response = client.get(
        reverse("profile"),
        HTTP_AUTHORIZATION=f" Token {token}",
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "name" in content and content.get("name") != profile.name
    ), f"name not found in response: {content}"
    assert (
        "email" in content and content.get("email") != profile.user.email
    ), f"email not found in response: {content}"
    assert (
        "first_name" in content and content.get("first_name") != profile.user.first_name
    ), f"first_name not found in response: {content}"
    assert (
        "last_name" in content and content.get("last_name") != profile.user.last_name
    ), f"last_name not found in response: {content}"
    assert (
        "avatar_url" in content and content.get("avatar_url") != profile.avatar_url
    ), f"avatar_url not found in response: {content}"

    # Remove test images
    remove_test_images()
