"""Module containing UI tests for the application base."""


def test_home(driver):
    """Test that the home page is correctly displayed when logged in."""
    driver.get("http://localhost:8000/")

    assert driver.find_element_by_id("home_heading").text == "Process Automation Tools - Home"
    assert driver.find_element_by_id("card_title_expense_refund").text == "Expense Refund"
    assert driver.find_element_by_id("card_description_expense_refund").text == \
        "Request to have your expenses refunded."


def test_navigation(driver):
    """Test that the navigation bar is correctly displayed."""
    driver.get("http://localhost:8000/")

    assert driver.find_element_by_id("btn-nav-home").text == "Home"
    assert driver.find_element_by_id("btn-nav-refund").text == "Expense Refund"


def test_logout(driver):
    """Test that the logged out page is correctly displayed."""
    driver.get("http://localhost:8000/logout/")

    assert driver.find_element_by_id("text-logged-out").text == "You have been successfully " \
                                                                "logged out."
    assert driver.find_element_by_id("btn-login").text == "Log in"
