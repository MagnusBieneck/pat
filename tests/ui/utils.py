"""Contains utils for the UI tests."""
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


_URL_PREFIX = "http://localhost:8000"


def get_webdriver():
    """Returns an instance of the selenium web driver."""
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("intl.accept_languages", "en")

    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.implicitly_wait(1)

    return driver


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

    def login(self):
        """Function to log in, serves as test case at the same time to verify that login works."""
        self.get("/")

        username = self.element("text-username")
        password = self.element("password-password")

        assert username
        assert password

        username.send_keys("tester")
        password.send_keys("tester")
        password.send_keys(Keys.RETURN)

        assert self.element("btn-logout")
