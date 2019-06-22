"""Module containing tests concerning the user authentication/authorisation."""
import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.parametrize("route", [
    "/",
    "/refund/",
    "/refund/new/"
])
def test_login_required(route):
    """Test that all pages where login is required  redirect to login page."""
    client = Client()

    response = client.get(route)
    assert response.status_code == 302
