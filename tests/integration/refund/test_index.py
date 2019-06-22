"""Module containing tests for the refund request index page."""
from django.test import Client
import pytest


@pytest.mark.django_db
def test_index():
    """Test that the index page appears correctly."""
    client = Client()
    response = client.get("/refund/")

    assert response.status_code == 200
    assert any([template.name == "refund/index.html" for template in response.templates])
