"""Contains utils for the UI tests."""
from django.test import LiveServerTestCase
from selenium import webdriver


_URL_PREFIX = "http://localhost:8000"


def get_webdriver():
    """Returns an instance of the selenium web driver."""
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("intl.accept_languages", "en")

    return webdriver.Firefox(firefox_profile=firefox_profile)


class DjangoSeleniumTest(LiveServerTestCase):
    """Base class for all UI tests in this project."""

    def setUp(self):
        """Sets up the necessary environment for the test cases."""
        self.selenium = get_webdriver()
        super(DjangoSeleniumTest, self).setUp()

    def tearDown(self):
        """Tears down the testing environment."""
        self.selenium.quit()
        super(DjangoSeleniumTest, self).tearDown()

    def get(self, route):
        """Shortcut function for selenium.get()."""
        self.selenium.get(_URL_PREFIX + route)

    def element(self, id_):
        """Shortcut function for selenium.find_element_by_id()."""
        return self.selenium.find_element_by_id(id_)
