from django.urls import reverse
import pytest
from scripts.make_user import create_profile


@pytest.mark.django_db
def test_logout(client):
    """Check logout"""
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ))
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert response.status_code == 200, f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Logout
    response = client.post(
        reverse("logout"),
        HTTP_AUTHORIZATION=f" Token {token}",
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 200, f"Response status code: {response.status_code} and content: {content}"
    assert "response" in content and content.get("response") == "Cierre de sesión completado", f"Error not found in response: {content}"


@pytest.mark.django_db
def test_logout_error_not_send_token(client):
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ))
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 200, f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Logout
    response = client.post(
        reverse("logout"),
        HTTP_AUTHORIZATION="",
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 401, f"Response status code: {response.status_code} and content: {content}"
    assert "detail" in content and content.get("detail") == "Las credenciales de autenticación no se proveyeron.", f"Error not found in response: {content}"


@pytest.mark.django_db
def test_logout_error_wrong_token(client):
    # Given
    profile = create_profile(add_image=False)

    # When
    # Get token
    response = client.post(
        reverse("login"),
        data=dict(
            email=profile.user.email,
            password="password",
        ))
    # Get content
    content = response.json()
    token = content.get("token")

    # Then
    assert response.status_code == 200, f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content, f"Token not found in response: {content}"

    # When
    # Logout
    response = client.post(
        reverse("logout"),
        HTTP_AUTHORIZATION=f" Token {token}a",
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 401, f"Response status code: {response.status_code} and content: {content}"
    assert "detail" in content and content.get("detail") == "Token inválido.", f"Error not found in response: {content}"
