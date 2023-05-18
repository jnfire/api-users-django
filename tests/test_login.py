from django.urls import reverse
import pytest
from scripts.make_users import create_profile


@pytest.mark.django_db
def test_login(client):
    """Check login"""
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

    # Then
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"


@pytest.mark.django_db
def test_login_wrong_password(client):
    """Check login with wrong password"""
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="wrong_password",
        ),
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 401
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "response" in content and content.get("response") == "Contraseña no valida"
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_login_wrong_email(client):
    """Check login with wrong email"""
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=f"a{profile.user.email}",
            password="password",
        ),
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 404
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "response" in content
        and content.get("response") == "El email no es valido o no existe"
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_login_inactive_user(client):
    """Check login with inactive user"""
    # Given
    profile = create_profile(add_image=False)
    profile.user.is_active = False
    profile.user.save()

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

    # Then
    assert (
        response.status_code == 403
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "response" in content and content.get("response") == "Usuario no activo"
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_login_wrong_method(client):
    """Check login with wrong method"""
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.get(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ),
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 405
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "detail" in content and content.get("detail") == 'Método "GET" no permitido.'
    ), f"Error not found in response: {content}"


@pytest.mark.django_db
def test_login_empty_fields(client):
    """Check login with empty fields"""
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email="",
            password="",
        ),
    )
    # Get content
    content = response.json()

    # Then
    assert (
        response.status_code == 400
    ), f"Response status code: {response.status_code} and content: {content}"
    assert (
        "email" in content
        and content.get("email")[0] == "Este campo no puede estar en blanco."
    ), f"Error not found in response: {content}"
    assert (
        "password" in content
        and content.get("password")[0] == "Este campo no puede estar en blanco."
    ), f"Error not found in response: {content}"
