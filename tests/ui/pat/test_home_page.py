"""Module containing UI tests for the home page."""
from django.test import LiveServerTestCase
from selenium import webdriver


class TestHome(LiveServerTestCase):
    """Wrapper class for the test cases."""

    def setUp(self):
        """Sets up the necessary environment for the test cases."""
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", "en")

        self.selenium = webdriver.Firefox(firefox_profile=firefox_profile)
        super(TestHome, self).setUp()

    def tearDown(self):
        """Tears down the testing environment."""
        self.selenium.quit()
        super(TestHome, self).tearDown()

    def test_home(self):
        """Test that the home page is correctly displayed."""
        selenium = self.selenium

        selenium.get("http://localhost:8000/")

        assert selenium.find_element_by_id("home_heading").text == "Process Automation Tools - Home"
        assert selenium.find_element_by_id("card_title_expense_refund").text == "Expense Refund"
        assert selenium.find_element_by_id("card_description_expense_refund").text == \
            "Request to have your expenses refunded."
