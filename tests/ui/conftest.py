"""Modules containing fixtures for the UI tests."""
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


CREDENTIALS = {
    "standard": ("tester-standard", "tester-standard"),
    "staff": ("tester-staff", "tester-staff"),
    "superuser": ("tester-superuser", "tester-superuser")
}


def get_webdriver():
    """Returns an instance of the selenium web driver."""
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("intl.accept_languages", "en")

    instance = webdriver.Firefox(firefox_profile=firefox_profile)
    instance.implicitly_wait(1)

    return instance


def create_driver(login=False, role="standard"):
    """Returns an instance of the Selenium web driver."""
    instance = get_webdriver()

    if login:
        instance.get("http://localhost:8000/")
        username, password = CREDENTIALS[role]

        username_field = instance.find_element_by_id("text-username")
        password_field = instance.find_element_by_id("password-password")

        assert username_field
        assert password_field

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        assert instance.find_element_by_id("btn-logout")

    return instance


@pytest.fixture
def driver():
    """Return a driver without any login."""
    instance = create_driver()
    yield instance
    instance.quit()


@pytest.fixture
def driver_standard():
    """Return a driver and login as standard user."""
    instance = create_driver(login=True, role="standard")
    yield instance
    instance.quit()


@pytest.fixture
def driver_staff():
    """Return a driver and login as staff user."""
    instance = create_driver(login=True, role="staff")
    yield instance
    instance.quit()


@pytest.fixture
def driver_superuser():
    """Return a driver and login as superuser."""
    instance = create_driver(login=True, role="superuser")
    yield instance
    instance.quit()
