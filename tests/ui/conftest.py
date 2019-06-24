"""Modules containing fixtures for the UI tests."""
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_webdriver():
    """Returns an instance of the selenium web driver."""
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("intl.accept_languages", "en")

    instance = webdriver.Firefox(firefox_profile=firefox_profile)
    instance.implicitly_wait(1)

    return instance


@pytest.fixture
def driver(login=True):
    """Returns an instance of the Selenium web driver."""
    instance = get_webdriver()

    if login:
        instance.get("http://localhost:8000/")

        username = instance.find_element_by_id("text-username")
        password = instance.find_element_by_id("password-password")

        assert username
        assert password

        username.send_keys("tester")
        password.send_keys("tester")
        password.send_keys(Keys.RETURN)

        assert instance.find_element_by_id("btn-logout")

    yield instance
    instance.quit()
