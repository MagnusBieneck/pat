"""Module containing integration tests for the home page."""
import pytest


@pytest.mark.django_db
def test_home(login, client):  # pylint: disable=unused-argument
    """Test that the home page is displayed correctly."""
    response = client.get("/")

    assert response.status_code == 200
    assert any([template.name == "home.html" for template in response.templates])
