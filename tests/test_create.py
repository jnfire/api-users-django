from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_create_user(client):
    """Check create user"""
    # Given
    response = client.post(
        reverse("create"),
        data=dict(
            email="test@test.com",
            password="password",
        )
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 201, f"Response status code: {response.status_code} and content: {content}"


@pytest.mark.django_db
def test_create_user_error_email_already_exists(client):
    """Check create user with email already exists"""
    # Given
    response = client.post(
        reverse("create"),
        data=dict(
            email="test@test.com",
            password="password",
        )
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 201, f"Response status code: {response.status_code} and content: {content}"

    # When
    response = client.post(
        reverse("create"),
        data=dict(
            email="test@test.com",
            password="password",
        )
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 400, f"Response status code: {response.status_code} and content: {content}"
    assert "response" in content and content.get("response") == "El usuario ya existe", f"Error not found in response: {content}"


@pytest.mark.django_db
def test_create_and_login(client):
    """Check login"""
    # Given
    response = client.post(
        reverse("create"),
        data=dict(
            email="test@test.com",
            password="password",
        )
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 201, f"Response status code: {response.status_code} and content: {content}"

    # When
    response = client.post(
        reverse("login"),
        data=dict(
            email="test@test.com",
            password="password",
        )
    )
    # Get content
    content = response.json()

    # Then
    assert response.status_code == 200, f"Response status code: {response.status_code} and content: {content}"
    assert "token" in content and content.get("token") != "", f"Token not found in response: {content}"

