"""Module containing UI tests for the home page."""
from tests.ui.utils import DjangoSeleniumTest


class TestHome(DjangoSeleniumTest):
    """Wrapper class for the test cases."""

    def test_home(self):
        """Test that the home page is correctly displayed."""
        self.get("/")

        assert self.element("home_heading").text == "Process Automation Tools - Home"
        assert self.element("card_title_expense_refund").text == "Expense Refund"
        assert self.element("card_description_expense_refund").text == \
            "Request to have your expenses refunded."
