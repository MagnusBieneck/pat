"""Module containing UI tests for the application base."""
from tests.ui.utils import DjangoSeleniumTest


class TestPAT(DjangoSeleniumTest):
    """Wrapper class for the test cases."""

    def test_home(self):
        """Test that the home page is correctly displayed when logged in."""
        self.login()
        self.get("/")

        assert self.element("home_heading").text == "Process Automation Tools - Home"
        assert self.element("card_title_expense_refund").text == "Expense Refund"
        assert self.element("card_description_expense_refund").text == \
            "Request to have your expenses refunded."

    def test_navigation(self):
        """Test that the navigation bar is correctly displayed."""
        self.login()
        self.get("/")

        assert self.element("btn-nav-home").text == "Home"
        assert self.element("btn-nav-refund").text == "Expense Refund"

    def test_logout(self):
        """Test that the logged out page is correctly displayed."""
        self.login()
        self.get("/logout/")

        assert self.element("text-logged-out").text == "You have been successfully logged out."
        assert self.element("btn-login").text == "Log in"
