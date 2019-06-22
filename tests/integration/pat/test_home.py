"""Module containing integration tests for the home page."""
from django.test import Client


def test_home():
    """Test that the home page is displayed correctly."""
    client = Client()
    response = client.get("/")

    assert response.status_code == 200
    assert any([template.name == "home.html" for template in response.templates])
