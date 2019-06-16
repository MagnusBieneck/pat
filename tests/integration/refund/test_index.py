"""Module containing tests for the refund request index page."""
from django.test import TransactionTestCase, Client


class TestRefundIndex(TransactionTestCase):
    """Wrapper class for test cases."""

    def test_index(self):  # pylint: disable=no-self-use
        """Test that the index page appears correctly."""
        client = Client()
        response = client.get("/refund/")

        assert response.status_code == 200

        # These tests should be refined using a sophisticated HTML testing method (GitHub issue #18)
        assert "Request Overview" in str(response.content)
        assert "<table" in str(response.content)
