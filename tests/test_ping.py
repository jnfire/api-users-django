from django.urls import reverse

# Test ping
def test_ping(client):
    """Check service ping"""
    url = reverse("ping")
    response = client.get(url)
    content = response.json()
    assert response.status_code == 200
    assert content["response"] == "pong!"
