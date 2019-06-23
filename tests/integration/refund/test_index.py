"""Module containing tests for the refund request index page."""
import pytest


@pytest.mark.django_db
def test_index(login, client):  # pylint: disable=unused-argument
    """Test that the index page appears correctly."""
    response = client.get("/refund/")

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
