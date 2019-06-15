"""Module containing integration tests for the home page."""
from django.test import TransactionTestCase, Client


class TestHome(TransactionTestCase):
    """Wrapper class for the test cases."""

    def test_home(self):
        """Test that the home page is displayed correctly."""
        client = Client()
        response = client.get("/")

        assert response.status_code == 200
        self.assertTemplateUsed("templates/home.html")

        elements = [
            '<h5 class="card-title">Expense Refund</h5>',
            '<a href="/refund/" class="card-link">Form</a>'
        ]
        for element in elements:
            self.assertInHTML(element, str(response.content))
