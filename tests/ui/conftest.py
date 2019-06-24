"""Modules containing fixtures for the UI tests."""
import pytest
from selenium.webdriver.common.keys import Keys
from tests.ui.utils import get_webdriver


@pytest.fixture
def webdriver(login=True):
    """Returns an instance of the Selenium web driver."""
    driver = get_webdriver()

    if login:
        driver.get("http://localhost:8000/")

        username = driver.find_element_by_id("text-username")
        password = driver.find_element_by_id("password-password")

        assert username
        assert password

        username.send_keys("tester")
        password.send_keys("tester")
        password.send_keys(Keys.RETURN)

        assert driver.find_element_by_id("btn-logout")

    yield driver
    driver.quit()
