"""Module containing tests for the refund request index page."""
from django.test import TransactionTestCase, Client


class TestRefundIndex(TransactionTestCase):
    """Wrapper class for test cases."""

    def test_index(self):  # pylint: disable=no-self-use
        """Test that the index page appears correctly."""
        client = Client()
        response = client.get("/refund/")

        assert response.status_code == 200
        self.assertTemplateUsed(response, "refund/index.html")
